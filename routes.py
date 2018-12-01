from functools import wraps
from flask import request, render_template, url_for, redirect
from flask_login import current_user, login_required, login_user, logout_user
from server import app, valid_time, sys, login_manager, days
from src.healthCareCentre import *
from src.healthProvider import *
from src.Appointment import *
import time
import datetime as dt
import csv


'''
this is for unauthorised access
'''
@app.route('/401')
@app.errorhandler(401)
def unauthorised_access(e=None):
    return render_template('401.html'),401

@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'),404 

@login_manager.user_loader
def load_user(email):
    return sys.get_user(email)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if authenticate_user(email, password) == True:
            if sys.is_provider(email, password) == True:
                isProvider = True
                return redirect(url_for('view_appointments'))
            else:
                return redirect(url_for('search'))

    return render_template('login.html')

def authenticate_user(email, password):
    if sys._user_manager.verify_user(email, password) == True:
        user = sys.get_user(email)
        login_user(user)
        return True
    return False
        
@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('login'))


@app.route('/health_centre/<name>', methods=['GET','POST'])
@login_required
def view_centre(name):

    if current_user.is_authenticated != True:
        abort(401)

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)
    isProvider = False
    if sys.is_provider(curr_user_email, curr_user.get_password()):
        isProvider = True
    
    if request.method == "POST":
        if 'rating' in request.form:
            centre = sys.get_centre(name)
            new_rating = request.form['rating']
            feedback = request.form['feedback']
            sys.add_rating(centre, new_rating, feedback, curr_user)

            Data = []
            row = []
            row.append(centre.get_name())
            row.append(new_rating)
            row.append(feedback)
            row.append(curr_user.get_id())
            Data.append(row)
            myFile = open('ratings.csv','a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(Data)
        else:
            chosen_provider = request.form["provider"]
            provider = sys.get_provider(chosen_provider)
            return redirect(url_for('view_available_bookings', centre = name, provider = chosen_provider))

    centre = sys.get_centre(name)
    providers = centre.get_providers()
    noProviders = False
    if centre.num_providers() == 0:
        noProviders = True
    return render_template('profiles/centre_profile.html', centre = centre, is_provider = isProvider, ratings = centre.get_ratings(),noProviders=noProviders)


@app.route('/health_provider/<name>', methods=['GET','POST'])
@login_required
def view_provider(name):
    if current_user.is_authenticated != True:
        abort(401)

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)
    isProvider = False
    if sys.is_provider(curr_user_email, curr_user.get_password()):
        isProvider = True

    Provider = sys.get_providers_by_name(name)[0]
    ProviderCentres = Provider.get_centres()
    noCentres = False
    if Provider.num_centres() == 0:
        noCentres = True

    curr_ratings = Provider.get_ratings()
    if curr_ratings == None:
        curr_ratings = False

    if request.method == "POST":
        if 'rating' in request.form:
            new_rating = request.form['rating']
            feedback = request.form['feedback']
            sys.add_rating(Provider, new_rating, feedback, curr_user)

            Data = []
            row = []
            row.append(Provider.get_id())
            row.append(new_rating)
            row.append(feedback)
            row.append(curr_user.get_id())
            Data.append(row)
            myFile = open('ratings.csv','a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(Data)
        else:
            chosen_centre = request.form["centre"]
            return redirect(url_for('view_available_bookings', centre = chosen_centre, provider = name))

    return render_template('profiles/provider_profile.html', provider = Provider, centres = ProviderCentres, is_provider = isProvider, ratings = curr_ratings, noCentres=noCentres)



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    if current_user.is_authenticated != True:
        abort(401)

    results = []

    if request.method == 'POST':
        searchWord = str(request.form["search_input"])
        option = str(request.form["searchRadio"])
        service = str(request.form["service"])
        
        
        
        if not searchWord:
            if option == "centreName":
                results = sys.get_all_centres()
                return render_template("search.html", message = "Please enter a centre name", results = results, category = option)
            elif option == "centreLocation":
                results = sys.get_all_centres()
                return render_template("search.html", message = "Please enter a Location", results = results, category = option)
            elif option == "providerName":
                results = sys.get_all_providers()
                return render_template("search.html", message = "Please enter a provider name", results = results, category = option)
        else:
            results = sys.search_system(searchWord,service,option)
            
            if not results:
                return render_template("search.html", noresult = True, results = [], category = option)
            else:
                return render_template("search.html", results = results, category = option)

    return render_template('search.html', results = results)


@app.route('/book', methods=['GET', 'POST'])
@login_required
def view_available_bookings():
    if current_user.is_authenticated != True:
        abort(401)

    if request.method == "GET":
        provider = request.args['provider']
        centre = request.args['centre']
        chosen_provider = sys.get_providers_by_name(provider)[0]
        chosen_centre = sys.get_centre(centre)

        # get working hours at centre
        workplace = chosen_provider.get_workplace(centre)

        print(provider)
        print(workplace.get_centre_name())
        print(workplace.get_start_hours())
        print(workplace.get_end_hours())

        return render_template('booking.html', profile=chosen_provider, centre=chosen_centre, days=days, roster=workplace.get_roster(), n_days=len(days))

    return render_template('base.html')

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def view_appointments():
    if current_user.is_authenticated != True:
        abort(401)

    if request.method == "POST":

        if 'details' in request.form:
            session = request.form['details']
            return redirect(url_for('view_session_details', session = session))
        
        providerEmail = request.form['provider_email']
        time = request.form['time_slot']
        day = request.form['day']
        centreName = request.form['centre_name']
        reason = request.form['booking_reason']
        curr_user_email = current_user.get_id()
        curr_user = sys.get_user(curr_user_email)
        
        already = False
        #start reading the file
        with open('appointment.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            new_list = list(csv_reader)
            if len(new_list) != 0:

                #check if the provider is booked on the same day ,same time,same centrename, same current user
                for i in new_list:
                    if str(i[0]) == str(providerEmail) and str(i[1]) == str(time) and str(i[2]) == str(day) and str(i[3]) == str(centreName) and str(i[4])==str(curr_user.get_id()):
                        already = True
                        break

                #check if the provider is booked on the same day ,same time,same centrename

                for i in new_list:
                    if str(i[0]) == str(providerEmail) and str(i[1]) == str(time) and str(i[2]) == str(day) and str(i[3]) == str(centreName):
                        already = True
                        break
                #check if the provider is booked on the same day ,same time for providers with more than 1 centres

                for i in new_list:
                    if str(i[0]) == str(providerEmail) and str(i[1]) == str(time) and str(i[2]) == str(day):
                        already = True
                        break
                #check if the current user has an appointment in the same tikme and the same day
                for i in new_list:
                    if  str(i[1]) == str(time) and str(i[2]) == str(day) and str(i[4])==str(curr_user.get_id()):
                        already = True
                        break

        #end reading the file
        if already == False:
            #start of writing to csv file
            Data = []
            row = []
            row.append(providerEmail)
            row.append(time)
            row.append(day)
            row.append(centreName)
            row.append(curr_user.get_id())
            row.append(reason)
            Data.append(row)
            myFile = open('appointment.csv','a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(Data)
            # end of writing to csv file

            sys.add_appointment(day, time, centreName, providerEmail, curr_user_email, days, reason)
            appointment_list = set(curr_user.get_future_apps())
            for i in appointment_list:
                print(i.get_provider().get_id())

            isProvider = False
            return render_template('appointments.html', appointments = appointment_list, isProvider = isProvider)
        
        if curr_user.get_future_apps() == False:
            appointmentss = []

        return render_template('appointments.html', appointments = False, isProvider = False, view=False)

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)

    if curr_user.get_future_apps() != False:
        appointment_list = curr_user.get_future_apps()
    else:
        appointment_list = False

    with open('past_appointment.csv') as csv_file5:
        csv_reader5 = csv.reader(csv_file5,delimiter=',')
        newlist = list(csv_reader5)

    if appointment_list != False:
        for i in appointment_list:
                for row in newlist:
            # may need more strict conditions i.e name of provider and name of patient
                    if i.get_date() == row[0] and i.get_time() == row[1] and i.get_patient().get_id() == row[4] and i.get_provider().get_id() == row[3]:
                        print(i.get_time() + " " + i.get_date() + " " + i.get_patient().get_id() + " " + i.get_provider().get_id())
                        appointment_list.remove(i)
                        break
        appointment_list = set(appointment_list)
            
    print("list of all future appointments")
    if appointment_list != False:
        print(len(appointment_list))
        for i in appointment_list:
            print(i.get_time() + " " + i.get_date() + " " + i.get_patient().get_id() + " " + i.get_provider().get_id())

    isProvider = False
    if sys.is_provider(curr_user_email, curr_user.get_password()):
        isProvider = True
    return render_template('appointments.html', appointments = appointment_list, isProvider = isProvider,view=True)

@app.route('/session', methods=['GET', 'POST'])
@login_required
def view_session_details():
    if request.method == 'POST':
        # get input from page and save it
        # get user's appointment list
        curr_user_email = current_user.get_id()
        curr_user = sys.get_user(curr_user_email)
        user_appointments = curr_user.get_future_apps()
        if user_appointments != False:
            appointments = list(user_appointments)
        
        # get input from page
        final = 0
        meds = []
        for arg in request.form:
            if final == 0:
                session = int(request.form[arg])
            else:
                meds.append(request.form.getlist(arg))
            final = final + 1
    
        # get current appointment
        # session = int(meds.pop(0)) # first element in form
        curr_appt = appointments[session]
        # we need to find this appointment 
        # 
        
        meds.pop() # remove blank value
        
        # last element in form is notes
        notes = meds.pop()
        
        # save to appoitnment's instance
        # create visit info class
        sess_info = VisitInfo(meds,notes)
        curr_appt.add_visit_info(sess_info)

        Data = []
        row = []
        row.append(curr_appt.get_date())
        row.append(curr_appt.get_time())
        row.append(curr_appt.get_centre().get_name())
        row.append(curr_appt.get_provider().get_id())
        row.append(curr_appt.get_patient().get_id())
        row.append(curr_appt.get_reason())
        row.append(curr_appt.get_visit_info().get_notes()[0])
        row.append(curr_appt.get_visit_info().get_medicines())

        Data.append(row)
        myFile = open('past_appointment.csv','a')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(Data)

        providerObj = sys.get_provider(curr_appt.get_provider().get_id())
        patientObj = sys.get_patient(curr_appt.get_patient().get_id())
        patientApps = patientObj.get_future_apps()
        providerApps = providerObj.get_future_apps()

        for i in patientApps:
            if curr_appt.get_date() == i.get_date() and curr_appt.get_time() == i.get_time():
                patientApps.remove(i)

        for i in providerApps:
            if curr_appt.get_date() == i.get_date() and curr_appt.get_time() == i.get_time():
                print("provider app to be removed")
                print(i.get_date() + " " + i.get_time() + " " + i.get_provider().get_id() + " " + i.get_patient().get_id())
                providerApps.remove(i)

        print("Current provider apps")
        for i in providerApps:
            print(i.get_time() + " " + i.get_date() + " " + i.get_patient().get_id() + " " + i.get_provider().get_id())

    
        #delete appointment from appointment.csv
        new_data = []
        with open('appointment.csv') as csv_file5:
            csv_reader5 = csv.reader(csv_file5,delimiter=',')
            newlist = list(csv_reader5)
            for row in newlist:
                print(row)
                # may need more strict conditions i.e name of provider and name of patient
                #if curr_appt.get_date() != row[2] or curr_appt.get_time() != row[1]:
                #if curr_appt.get_date() == row[2] and curr_appt.get_time() == row[1] and providerObj.get_id() == row[0]:
                 #   continue
                #else:   
                compare1 = str(curr_appt.get_date()) + str(curr_appt.get_time()) + str(providerObj.get_id())
                compare2 = str(row[2]) + str(row[1]) + str(row[0])
                if compare1 != compare2:
                    new_data.append(row)
        myFile = open('appointment.csv','w')
        with myFile:
            writer = csv.writer(myFile)
            print(new_data)
            writer.writerows(new_data)
                
        

        providerObj.add_past_app(curr_appt)
        patientObj.add_past_app(curr_appt)

        patient_past = providerObj.get_past_apps()
        provider_past = patientObj.get_past_apps()
        print("patient")
        for i in patient_past:
            print(i.get_time())
        print("provider")
        for j in provider_past:
            print(j.get_time())

        return redirect(url_for('view_appointments'))

    session = int(request.args['session'])

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)
    user_appointments = curr_user.get_future_apps()
    appointments = list(user_appointments)

    curr_appt = appointments[session]

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # needs to be edited to display info if it has already been saved
    return render_template('session_details.html', index=session, appointment=curr_appt)

@app.route('/past_appointments', methods=['GET', 'POST'])
@login_required
def past_appointments():
    if current_user.is_authenticated != True:
        abort(401)

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)

    if curr_user.get_past_apps() != False:
        appointment_list = set(curr_user.get_past_apps())
    else:
        appointment_list = False


    isProvider = False
    if sys.is_provider(curr_user_email, curr_user.get_password()):
        isProvider = True
    return render_template('past_appointments.html', PastAppointments = appointment_list, isProvider = isProvider,view=True)
    #return render_template("past_appointments.html")

@app.route('/patient_past_appointments/<patient>')
@login_required
def view_patient_history(patient):
    print("\n\n\n\n\n\n\n\n\n\n")
    print(patient)
    if current_user.is_authenticated != True:
        abort(401)

    curr_user_email = current_user.get_id()
    curr_user = sys.get_user(curr_user_email)

    patient = sys.get_user(patient)


    if patient.get_past_apps() != False:
        appointment_list = set(patient.get_past_apps())
    else:
        appointment_list = False

    return render_template('past_appointments.html', PastAppointments = appointment_list,view=True,pHistory=True,patient=patient)
    #return render_template("past_appointments.html")

