from src.CentreManager import CentreManager
from src.userManager import UserManager
from src.AppointmentManager import *

from src.workplace import *
from src.healthCareCentre import *
from src.review import *

class System:
    'System class'
    def __init__(self):
        self._user_manager = UserManager()
        self._centre_manager = CentreManager()
        self._appointment_manager = AppointmentManager()

    # Setters
    def add_patient(self, name, password, email, phone, medicare):
        self._user_manager.add_patient(name, password, email, phone, medicare)

    def add_centre(self,name, ctype, suburb,city,state,street,streetnum,abn,phone):
        self._centre_manager.add_centre(name, ctype, suburb,city,state,street,streetnum,abn,phone)

    def add_provider(self, name, password, email, phone, provider_num, profession):
        self._user_manager.add_provider(name, password, email, phone, provider_num, profession)

    def add_workplace(self, providerEmail, centreName, start, end):
        centre = self._centre_manager.get_centre(centreName)
        workplace = WorkPlace(centre, start, end)
        provider = self._user_manager.get_provider(providerEmail)
        provider.add_workplace(workplace)

    def add_provider_to_centre(self, providerEmail, centreName):
        provider = self._user_manager.get_provider(providerEmail)

        if provider != False:
            centre = self._centre_manager.get_centre(centreName)
        
            if centre != False:
                centre.add_provider(provider)

    def add_provider_to_centre_test(self, provider, centre):
        centre.add_provider(provider)

    def add_rating(self, healthcp, rating, feedback, user):
        rating_val = int(rating)
        review = Review(user, feedback, rating_val)
        
        ratings = healthcp.get_ratings()
        
        if healthcp.get_ratings() == None:
            healthcp.add_rating(review)
            return
        else:
            for rating in ratings:
                if rating.get_reviewer() == user:
                    ratings.remove(rating)
                    healthcp.add_rating(review)
                    return

        healthcp.add_rating(review)

    # Appointment Manager
    def add_appointment(self, date, time, centreName, providerEmail, patientEmail, days, reason):
        provider = self._user_manager.get_provider(providerEmail)
        centre = self._centre_manager.get_centre(centreName)
        patient = self._user_manager.get_patient(patientEmail)
        
        
        centreList = provider.get_centres()
        if centreList != False:
            for cent in centreList:
                if centre.get_name() == cent.get_centre_name():
                    break
            print(cent.get_centre_name())
            
            slots = cent.get_roster()
            d = 0
            for day in slots:
                
                if str(days[d]) == str(date):
                    break
                d = d+1;
            
            for sess in day:
                
                if str(time) == str(sess.get_time().time()):
                    sess.set_booked()
                    break
                

        self._appointment_manager.add_appointment(date, time, centre, provider, patient, reason)
        appointments = self._appointment_manager.get_appointments()
        for i in appointments:
            if patient.get_name() == i.get_patient().get_name():
                patient.add_future_app(i)
            if provider.get_name() == i.get_provider().get_name():
                provider.add_future_app(i)

    def add_past_appointment(self, date, time, centreName, providerEmail, patientEmail, days, reason, visit_info, meds):
        provider = self._user_manager.get_provider(providerEmail)
        centre = self._centre_manager.get_centre(centreName)
        patient = self._user_manager.get_patient(patientEmail)
        
        
        centreList = provider.get_centres()
        if centreList != False:
            for cent in centreList:
                if centre.get_name() == cent.get_centre_name():
                    break
            print(cent.get_centre_name())
            
            slots = cent.get_roster()
            d = 0
            for day in slots:
                
                if str(days[d]) == str(date):
                    break
                d = d+1;
            
            for sess in day:
                
                if str(time) == str(sess.get_time().time()):
                    sess.set_booked()
                    break
                
        #print(meds)
        self._appointment_manager.add_past_appointment(date, time, centre, provider, patient, reason, visit_info, meds )
        appointments = self._appointment_manager.get_past_appointments()

        for i in appointments:
            if patient.get_name() == i.get_patient().get_name():
                patient.add_past_app(i)
            if provider.get_name() == i.get_provider().get_name():
                provider.add_past_app(i)


    # Getters
    def get_provider(self,name):
        return self._user_manager.get_provider(name)

    def get_patient(self,name):
        return self._user_manager.get_patient(name)

    def is_provider(self,email,password):
        return self._user_manager.is_provider(email, password)

    def get_user(self,email):
        if self._user_manager.get_provider(email):
            return self._user_manager.get_provider(email)

        else:
            return self._user_manager.get_patient(email)

    # list
    def get_all_providers(self):
        return(self._user_manager.get_providers())
    
    # list
    def get_all_patients(self):
        return(self._user_manager.get_patients())
    
    # list
    def get_all_centres(self):
        return(self._centre_manager.get_all_centres())
    
    # list
    def get_providers_by_name(self, name):
        return self._user_manager.get_providers_by_name(name)
    # list
    def get_providers_by_service(self, service):
        return self._user_manager.get_providers_by_service(service)

    def get_workplace_name(self,ProviderName):
        #list of object providers
        listProvider = self._user_manager.get_provider(str(ProviderName))
        new = listProvider.get_centres()
        return new
        
    def get_workplace_start_hours(self,ProviderName):
        listProvider = self._user_manager.get_provider(str(ProviderName))
        new = listProvider.get_centres()
        return new

    def get_workplace_end_hours(self,ProviderName):
        listProvider = self._user_manager.get_provider(str(ProviderName))
        new = listProvider.get_centres()
        return new

        
    # START centre finders            
    def get_centre_by_Location(self, location):
        return self._centre_manager.get_centre_by_location(CentreName)

    def get_centre_by_suburb(self, centreSuburb):
        return self._centre_manager.get_centres_by_suburb(centreSuburb)

    def get_centre(self, name):
        return self._centre_manager.get_centre(name)
    # END centre finders         


    def get_appointments(self):
        return self._appointment_manager.get_appointments()

    # Seach by input
    def search_system(self, input, service, search_option):
        results = []
        if search_option == "centreName":
            results = self._centre_manager.get_centres_part_name(input)
        elif search_option == "centreLocation":
            results = self.get_centre_by_suburb(input)
        elif search_option == "providerName":
            results = self._user_manager.get_providers_part_name(input)

        if service != "all":
            for result in results:
                if search_option == "centreName" or search_option == "centreLocation":
                    centre_services = result.get_services()
                    if service not in centre_services:
                        results.remove(result)
                else:
                    if service != result.get_profession():
                        results.remove(result)

        return results
