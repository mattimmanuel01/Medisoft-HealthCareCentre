from src.user import User

class Patient(User):
    '''A class which stores the patients information'''

    def __init__(self, name, password, email, phone, medicare):
        super().__init__(name, password, email, phone)
        self._medicare = medicare
        self._provider_list = []
        self._future_appointments = []
        self._past_appointments = []

    # Setters 
    def add_provider(self, Provider):
        self._provider_list.append(Provider)
        
    def add_future_app(self, Appointment):
        self._future_appointments.append(Appointment)

    def add_past_app(self, Appointment):
        self._past_appointments.append(Appointment)

    def add_past_app(self, Appointment):
        self._past_appointments.append(Appointment)

    # Getter
    def get_medicare(self):
        return self._medicare
    
    def get_provider_list(self):
        if self._provider_list == 0:
            return False
        else:
            return self._provider_list
    def get_future_apps(self):
        if len(self._future_appointments) == 0:
            return False
        else:
            return self._future_appointments
    

    def get_appointments(self):
        if self._appointment_list == 0:
            return False
        else:
            return self._appointment_list

    def get_past_apps(self):
        if len(self._past_appointments) == 0:
            return False
        else:
            return self._past_appointments
    

