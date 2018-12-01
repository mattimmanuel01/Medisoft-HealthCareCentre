class Appointment:
    def __init__(self, date, time, health_center, health_provider, patient, reason):
        self._date = date
        self._time = time
        self._health_center = health_center
        self._health_provider = health_provider
        self._visit_info = 'None'
        self._patient_info = patient
        self._reason = reason 

	#getters
    def get_date(self):
        return self._date

    def get_time(self):
        return self._time

    def get_centre(self):
        return self._health_center

    def get_provider(self):
        return self._health_provider

    def get_visit_info(self):
        return self._visit_info

    def get_patient(self):
        return self._patient_info
    
    def get_reason(self): # ready to go
        return self._reason

    def add_visit_info(self, VisitInfo):
        self._visit_info = VisitInfo

        

class VisitInfo:
    def __init__(self, medicines, notes):
        self._medicines = (medicines)
        self._notes = notes

    #setters
    def set_notes(self,notes):
        self._notes = notes

    #getters
    def get_notes(self):
        return self._notes

    def get_medicines(self):
        return self._medicines
