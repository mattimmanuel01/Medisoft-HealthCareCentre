from flask import Flask
from flask_login import LoginManager
from system import *
import csv
import datetime

# time
def valid_time(time):
    return time > 0

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'Another_highly_secret_key'

# Initiate login clas
login_manager = LoginManager()
login_manager.init_app(app)

# Initiate system class
sys = System()

#initialise next few days
base = datetime.datetime.today()
numdays = 10
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
days = []

for a in date_list:
    days.append(a.strftime('%A %d %B'))

# Add patients
with open('csv/patient.csv') as csv_file1:
    csv_reader1 = csv.reader(csv_file1,delimiter=',')
    for row in csv_reader1:
        sys.add_patient(row[0],row[2],row[1],row[3],row[4])

# Add providers
with open('csv/provider.csv') as csv_file3:
    csv_reader3 = csv.reader(csv_file3,delimiter=',')
    for row in csv_reader3:
        sys.add_provider(row[0],row[3],row[1],row[4],row[5],row[2])
        #name, password, email, phone, provider_num, profession

# Add centres
with open('csv/health_centres.csv') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    newlist = list(csv_reader)
    for row in newlist:
        sys.add_centre(row[0],row[1],row[4],row[5],row[5],row[6],row[7],row[2],row[3])

# Add list all affiliated providers to centre
with open('csv/provider_health_centre.csv') as csv_file2:
    csv_reader2 = csv.reader(csv_file2,delimiter=',')
    new_list = list(csv_reader2)

    sys.add_provider_to_centre(new_list[0][1],new_list[0][2])
    sys.add_provider_to_centre(new_list[1][1],new_list[1][2])
    sys.add_provider_to_centre(new_list[2][1],new_list[2][2])
    sys.add_provider_to_centre(new_list[3][1],new_list[3][2])
    sys.add_provider_to_centre(new_list[4][1],new_list[4][2])
    sys.add_provider_to_centre(new_list[5][1],new_list[5][2])
    sys.add_provider_to_centre(new_list[6][1],new_list[6][2])
    sys.add_provider_to_centre(new_list[7][1],new_list[7][2])
    sys.add_provider_to_centre(new_list[8][1],new_list[8][2])
    sys.add_provider_to_centre(new_list[9][1],new_list[9][2])
    sys.add_provider_to_centre(new_list[10][1],new_list[10][2])
    sys.add_provider_to_centre(new_list[11][1],new_list[11][2])



# add workplace (using centre and wrokhours)
with open('csv/provider_health_centre.csv') as csv_file2:
    csv_reader2 = csv.reader(csv_file2,delimiter=',')
    new_list = list(csv_reader2)
    sys.add_workplace("toby@gmail.com","Sydney Children Hospital",'12:00','13:00')
    sys.add_workplace(new_list[1][1],new_list[1][2],'13:00','15:00')
    sys.add_workplace(new_list[2][1],new_list[2][2],'14:00','15:00')
    sys.add_workplace(new_list[3][1],new_list[3][2],'16:00','17:00')
    sys.add_workplace(new_list[4][1],new_list[4][2],'18:00','19:00')
    sys.add_workplace(new_list[5][1],new_list[5][2],'12:00','13:00')
    sys.add_workplace(new_list[6][1],new_list[6][2],'12:00','16:00')
    sys.add_workplace(new_list[7][1],new_list[7][2],'12:00','18:00')
    sys.add_workplace(new_list[8][1],new_list[8][2],'12:00','19:00')
    sys.add_workplace(new_list[9][1],new_list[9][2],'12:00','13:00')
    sys.add_workplace(new_list[10][1],new_list[10][2],'12:00','14:00')
    sys.add_workplace(new_list[11][1],new_list[11][2],'12:00','15:00')


# Add time slots to workplace
def add_work_hours(providerEmail, centreName):
        centre_name = centreName
        profile = sys.get_provider(providerEmail)
        profilecentre = profile.get_centres()
        for i in profilecentre:
            if i.get_centre_name() == centre_name:
                rightWorkplace = i
                starthour = i.get_start_hours()
                endhour = i.get_end_hours()

        zero = dt.datetime.strptime('00:00', '%H:%M')
        thirty = dt.datetime.strptime('00:30', '%H:%M')
        i = dt.datetime.strptime(str(starthour.time()), '%H:%M:%S')
        end = dt.datetime.strptime(str(endhour.time()), '%H:%M:%S')

        now = datetime.datetime.now()

        first = False
        for day in days:
            times = []
            while(i != end):
                if first == False:
                    if now <= i:
                        times.append(i)
                    pass
                else:
                    times.append(i)
                i = (i - zero + thirty)
                #print(i.time())
            rightWorkplace.add_time_slots(times)
            i = dt.datetime.strptime(str(starthour.time()), '%H:%M:%S')
            first = True

add_work_hours("toby@gmail.com","Sydney Children Hospital")
add_work_hours("toby@gmail.com","UTS Health Service")
add_work_hours("samuel@gmail.com","Prince of Wales Hospital")
add_work_hours("sid@gmail.com","Royal Prince Alfred Hospital")
add_work_hours("michael@gmail.com","USYD Health Service")
add_work_hours("anna@gmail.com","UTS Health Service")
add_work_hours("thomas@gmail.com","Prince of Wales Hospital")
add_work_hours("ian@gmail.com","Sydney Children Hospital")
add_work_hours("gary@gmail.com","Sydney Children Hospital")
add_work_hours("anna@gmail.com","Sydney Children Hospital")
add_work_hours("anna@gmail.com","Prince of Wales Hospital")
add_work_hours("gary@gmail.com","USYD Health Service")


# add appointments
with open('appointment.csv') as csv_file5:
    csv_reader5 = csv.reader(csv_file5,delimiter=',')
    newlist = list(csv_reader5)
    for row in newlist:
        sys.add_appointment(row[2], row[1], row[3], row[0], row[4], days, row[5])
        #sys.add_appointment(self, date, time, centreName, providerEmail, patientEmail, days, reason);

# add past appointments
with open('past_appointment.csv') as csv_file6:
    csv_reader6 = csv.reader(csv_file6,delimiter=',')
    newlist = list(csv_reader6)
    for row in newlist:
        sys.add_past_appointment(row[0], row[1], row[2], row[3], row[4], days, row[5], row[6], row[7])
        #sys.add_appointment(self, date, time, centreName, providerEmail, patientEmail, days, reason, visit_info);

#add ratings
with open('ratings.csv') as csv_file7:
    csv_reader7 = csv.reader(csv_file7,delimiter=',')
    newlist = list(csv_reader7)
    for row in newlist:
        cp = sys.get_centre(row[0]) # centrename
        patient = sys.get_patient(row[3]) # patient email
        if cp == False:
            cp = sys.get_provider(row[0]) # provider email
        sys.add_rating(cp, row[1], row[2], patient)
