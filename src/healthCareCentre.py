from src.CentreType import *
from src.location import Location
from src.review import Review
from src.healthProvider import *

class HealthCareCentre:
    'A class containing the informtion of a healthcare centre'
    def __init__(self, name, ctype,suburb,city,state,street,streetnum,abn,phone):
        self._name = name
        self._type = CentreType(ctype).name
        self._health_providers = []
        self._ratings = []
        self._avg_rating = 'none'
        self._location = Location(suburb,city,state,street,streetnum)
        self._abn = abn
        self._phone = phone
        self._services_avail = []

	# Setters
    def add_provider(self, HealthProvider):
        self._services_avail.append(HealthProvider.get_profession)
        self._health_providers.append(HealthProvider)

    def add_rating(self, Review):
        self._ratings.append(Review)
        self.set_avg_rating()

    def set_avg_rating(self):
        total = 0
        for i in self._ratings:
            total += i._rating
        self._avg_rating = total/len(self._ratings)

    # Getters
    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def num_providers(self):
        print(len(self._health_providers))
        return len(self._health_providers)

    def get_providers(self):
        if len(self._health_providers) == 0:
            return "Centre has no providers"
        else:
            return self._health_providers

    def get_set_of_professions(self):
        if len(self._health_providers) == 0:
            return "Centre has no providers"
        else:
            services = []
            for i in self._health_providers:
                services.append(i.get_profession())
            return set(services)

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

    def get_location(self):
        return self._location

    def get_provider(self, name):
        if len(self._health_providers) == 0:
            return "Centre has no providers"
        else:
            for i in self._health_providers:
                if i.get_name() == name:
                    return i
                return "not found"

    def get_services(self):
        return self._services_avail

    def get_phone(self):
        return self._phone

    def get_abn(self):
        return self._abn

