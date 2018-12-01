from src.user import User
import datetime
from src.workplace import WorkPlace
from src.review import Review

class HealthProvider(User):
    'a class keeping all informationn relevant to a provider'
    def __init__(self, name, password, email, phone, provider_num, profession):
        super().__init__(name, password, email, phone)
        self._provider_num = provider_num
        self._profession = profession
        self._centres = []
        self._ratings = []
        self._avg_rating = 'None'
        self._past_appointments = []
        self._future_appointments = []

    # Setter Methods
    def add_rating(self, Review):
        self._ratings.append(Review)
        self.set_avg_rating()

    def set_avg_rating(self):
        total = 0
        print("this ran at least i think")
        for i in self._ratings:
            total += i._rating
        self._avg_rating = total/len(self._ratings)
        print(total)
        print(len(self._ratings))
    
    def add_future_app(self, Appointment):
        self._future_appointments.append(Appointment)

        #sorted(self._future_appointments, key=lambda x: datetime.datetime.strptime(x._date, '%I:%M%p %D/%M/%Y'))

    def add_past_app(self, Appointment):
        self._past_appointments.append(Appointment)

        #sorted(self._past_appoinments, key=lambda x: datetime.datetime.strptime(x._date, '%I:%M%p %D/%M/%Y'))

    def add_workplace(self, WorkPlace):
        self._centres.append(WorkPlace)


    # Getter Methods
    def num_centres(self):
        return len(self._centres)
        
    def get_profession(self):
        return self._profession

    def get_centres(self):
        if len(self._centres) == 0:
            return False
        else:
            return self._centres

    def get_workplace(self, workplace):
        print(workplace)
        for place in self._centres:
            print(place.get_centre_name())
            if place.get_centre_name() == workplace:
                return place

    def get_ratings(self):
        if len(self._ratings) == 0:
            return None
        else:
            return self._ratings

    def get_avg_rating(self):
        if self._avg_rating == 'None':
            return 'No rating yet'
        else:
            return self._avg_rating

    def get_past_apps(self):
        if len(self._past_appointments) == 0:
            return False
        else:
            return self._past_appointments

    def get_future_apps(self):
        if len(self._future_appointments) == 0:
            return False
        else:
            return self._future_appointments

    def __str__(self):
        return ""


class GP(HealthProvider):
    pass

class Physio(HealthProvider):
    pass

class Pharmacist(HealthProvider):
    pass

class Pathologist(HealthProvider):
    pass
        

# NOTES:
    '''def add_future_app(self, Appointment):
        self._future_appointments.append(Appointment)

        sorted(future_appoinments, key=lambda x: datetime.datetime.strptime(x._date, '%I:%M%p %D/%M/%Y'))

        for i in future_appointments:
            if i.date > date.today(): # this may just be i.date
                past_appointments.append(i)
                future_appointments.remove(i) '''
