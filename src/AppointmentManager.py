from src.Appointment import *

class AppointmentManager:
    appointments = [];
    def __init__(self):
        self._appointments = []
        self._past_appointments = []

    #setters
    def add_appointment(self, date, time, healthCenter, healthProvider, patient, reason):
        
        appointment = Appointment(date, time, healthCenter, healthProvider, patient, reason)

        self._appointments.append(appointment)
        
    def add_past_appointment(self, date, time, healthCenter, healthProvider, patient, reason, notes ,meds):
        appointment = Appointment(date, time, healthCenter, healthProvider, patient, reason)
        visit_info = VisitInfo(meds,notes)
        appointment.add_visit_info(visit_info)

        self._past_appointments.append(appointment)


    #getters
    def get_appointments(self):
        return self._appointments
    
    def get_past_appointments(self):
        return self._past_appointments
