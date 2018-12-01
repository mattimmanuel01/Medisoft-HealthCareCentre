import pytest
from flask_login import LoginManager
from system import *
from src.healthProvider import *
from src.healthCareCentre import *
import datetime
from src.AppointmentManager import *
from src.userManager import *
from flask import Flask
import csv



# classes used for testing
sys = System()

#initialise next few days
base = datetime.datetime.today()
numdays = 7
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
days = []

for a in date_list:
    days.append(a.strftime('%A %d %B'))

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

    for day in days:
        times = []
        while(i != end):
            times.append(i)
            i = (i - zero + thirty)
        rightWorkplace.add_time_slots(times)
        i = dt.datetime.strptime(str(starthour.time()), '%H:%M:%S')

# dummy patients
sys.add_patient("PatA","patA@gmail.com","cs1531","123456","MEDI1")
sys.add_patient("PatB","patB@gmail.com","cs1531","123456","MEDI2")
PatA = sys._user_manager._patients[0]
PatB = sys._user_manager._patients[1]

# dummy providers
sys.add_provider("ProvA","cs1531","ProvA@gmail.com","123456","PROVI1","GP")
sys.add_provider("ProvB","cs1531","ProvB@gmail.com","123456","PROVI2","GP")
ProvA = sys._user_manager._providers[0]
ProvB = sys._user_manager._providers[1]

sys.add_patient("Jack", "cs1531", "jack@gmail.com", "123456", "MED1")
sys.add_provider("Toby", "cs1531", "toby@gmail.com", "3232323", "PROV12", "Pathologist")

# dummy centres
sys.add_centre("CentA","Hospital","Randwick","Sydney","Sydney","doncaster","4","1111","33818763")
sys.add_centre("CentB","Hospital","Randwick","Sydney","Sydney","doncaster","3","1112","65260987")
sys.add_centre("CentC","MedicalCentre","Kensington","Sydney","Sydney","doncaster","12","1113","56795327")
CentA = sys._centre_manager._centre_list[0]
CentB = sys._centre_manager._centre_list[1]
CentC = sys._centre_manager._centre_list[2]


# add providers to centres
sys.add_provider_to_centre("ProvA@gmail.com","CentA")
sys.add_provider_to_centre("ProvA@gmail.com","CentB")
sys.add_provider_to_centre("ProvA@gmail.com","CentC")
sys.add_workplace("ProvA@gmail.com","CentA",'00:00','23:00')
sys.add_workplace("ProvA@gmail.com","CentB",'00:00','23:00')
sys.add_workplace("ProvA@gmail.com","CentC",'00:00','23:00')

sys.add_provider_to_centre("ProvB@gmail.com","CentA")
sys.add_provider_to_centre("ProvB@gmail.com","CentB")
sys.add_provider_to_centre("ProvB@gmail.com","CentC")
sys.add_workplace("ProvB@gmail.com","CentA",'00:00','23:00')
sys.add_workplace("ProvB@gmail.com","CentB",'00:00','23:00')
sys.add_workplace("ProvB@gmail.com","CentC",'00:00','23:00')

add_work_hours("ProvA@gmail.com","CentA")
add_work_hours("ProvA@gmail.com","CentB")
add_work_hours("ProvA@gmail.com","CentC")

add_work_hours("ProvB@gmail.com","CentA")
add_work_hours("ProvB@gmail.com","CentB")
add_work_hours("ProvB@gmail.com","CentC")

#adding characters longer than 1000 for reason is handles in front end and can't be run via pytest
#creating a booking before the current day is handles in front end and can't be run via pytest
#createing a booking with at the same time to a current appointment is handled in front end
class TestUSBookAppointment(object):

    # book same session twice handled by frontend
    # book twice in one day handled by frontend
    # book already booked session handled by frontend
    # invalid time input handled by frontend
    # provider booking appts handled by frontend
    


    # no reason input test
    def test_booking_succesful_no_reason(self):
        print("test successful - no reason input")
        reason = ""
        provider = ProvA
        patient = PatA
        centre = ProvA._centres[0]
        time = "12:00"
        date = "19-10-2018"

        sys.add_appointment( date, time, centre.get_centre_name(), provider.get_id(), patient.get_id(), days, reason)
        assert len(sys._appointment_manager._appointments[0]._reason) == 0
        assert (sys._appointment_manager._appointments[0]._health_center._name) == "CentA"
        assert (sys._appointment_manager._appointments[0]._health_provider._name) == "ProvA"
        assert (sys._appointment_manager._appointments[0]._date) == "19-10-2018"
        assert (sys._appointment_manager._appointments[0]._time) == "12:00"
        assert (sys._appointment_manager._appointments[0]._reason) == ""
        assert (sys._appointment_manager._appointments[0]._patient_info) == PatA
 
    # test with reason input
    def test_booking_succesful_reason(self):
        print("test successful - reason input")
        reason = "testing"
        provider = ProvA
        patient = PatA
        centre = ProvA._centres[0]
        time = "13:00"
        date = "19-10-2018"
        sys.add_appointment( date, time, centre.get_centre_name(), provider.get_id(), patient.get_id(), days, reason)

        assert len(sys._appointment_manager._appointments[1]._reason) == 7
        assert (sys._appointment_manager._appointments[1]._health_center._name) == "CentA"
        assert (sys._appointment_manager._appointments[1]._health_provider._name) == "ProvA"
        assert (sys._appointment_manager._appointments[1]._date) == "19-10-2018"
        assert (sys._appointment_manager._appointments[1]._time) == "13:00"
        assert (sys._appointment_manager._appointments[1]._reason) == "testing"
        assert (sys._appointment_manager._appointments[1]._patient_info) == PatA



#If the user has never made a booking with the provider that is handled in front end and can't be tested with pytets
class TestUSViewPatientHistory(object):

    #test is the list of past appointmetns = number of appointments made
    #test to see if the users name is in the list of past of appointments
    def test_view_patient_past_appointments(self):
        print("test successful - can view past appointments")
        print(ProvA.get_past_apps())
        
        reason = ""
        provider = ProvA
        patient = PatA
        centre = ProvA._centres[0]
        time = "13:00"
        date = "10-10-2018"

        sys.add_appointment( date, time, centre.get_centre_name(), provider.get_id(), patient.get_id(), days, reason)

        medication = ""
        notes = ""
        meds = [medication]
        sess_info = VisitInfo(meds,notes)
        curr_appt =  sys._appointment_manager._appointments[2]
        curr_appt.add_visit_info(sess_info)
        ProvA._past_appointments.append(ProvA._future_appointments.pop())
        appointment_list = (ProvA.get_past_apps())

        assert len(appointment_list) == 1
        assert ProvA.get_past_apps()[0]._patient_info == PatA
        assert ProvA.get_past_apps()[0]._health_center._name == "CentA"
        assert ProvA.get_past_apps()[0]._health_provider._name == "ProvA"
        assert ProvA.get_past_apps()[0]._date == "10-10-2018"
        assert ProvA.get_past_apps()[0]._time == "13:00"
        assert ProvA.get_past_apps()[0]._reason == ""
        assert ProvA.get_past_apps()[0]._patient_info == PatA
        

    def test_view_past_appointments_empty(self):
        print("test successful - empty list past appointments")

        appointment_list = (ProvB.get_past_apps())
        assert appointment_list == False



       #should be able to see all the past appointments the patietn made with the provider 



    
#adding characters longer than 100 for medication and 1000 for notes is handles in front end and can't be run via pytest
class TestUSManagePatientHistory(object):

    def test_add_medication(self):
        print("test successful - add medication only")
        notes = ""
        medication = "500mg Amoxicillin"
        meds = [medication]
        sess_info = VisitInfo(meds,notes)
        sys._appointment_manager._appointments[0].add_visit_info(sess_info)
        assert (sys._appointment_manager._appointments[0]._visit_info._medicines[0]) == medication
        
 
    def test_add_notes(self):
        print("test successful - add notes only")
        notes = "Patient required illness form"
        medication = ""
        meds = [medication]
        sess_info = VisitInfo(meds,notes)
        sys._appointment_manager._appointments[0].add_visit_info(sess_info)
        assert (sys._appointment_manager._appointments[0]._visit_info._notes) == notes
        

    def test_add_notes_and_medication(self):
        print("test successful - add notes and medication ")
        medication = "amoxicillin"
        notes = "Patient has upper respitory tract infection, amoxicillin was percribed, patients advised to follow up in 1 week"
        meds = [medication]
        sess_info = VisitInfo(meds,notes)
        sys._appointment_manager._appointments[1].add_visit_info(sess_info)
        assert (sys._appointment_manager._appointments[1]._visit_info._notes) == notes
        assert (sys._appointment_manager._appointments[1]._visit_info._medicines[0]) == medication

    def test_add_nothing(self):
        print("test successful - add nothing ")
        notes = ""
        medication = ""
        meds = [medication]
        sess_info = VisitInfo(meds,notes)
        sys._appointment_manager._appointments[2].add_visit_info(sess_info)
        assert (sys._appointment_manager._appointments[2]._visit_info._notes) == notes
        assert (sys._appointment_manager._appointments[2]._visit_info._medicines[0]) == medication











