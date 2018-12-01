from src.healthCareCentre import *

class CentreManager:
    #Class which stores a list of centres and carries out centre related methods
    def __init__(self):
        self._centre_list = []

    # Setters
    def add_centre(self, name, ctype,suburb,city,state,street,streetnum,abn,phone):
        healthCentre = HealthCareCentre(name, ctype, suburb,city,state,street,streetnum,abn,phone)
        self._centre_list.append(healthCentre)

    # Getters
    def get_centre(self, name):
        for i in self._centre_list:
            if name.lower() in i.get_name().lower():
                return i
        return False
    
    
    def get_all_centres(self):
        return self._centre_list
    
    #list of partial matches to name
    def get_centres_part_name(self, name):
        results = []
        if len(self._centre_list) != 0:
            l_name = name.lower()
            for i in self._centre_list:
                curr = i.get_name().lower()
                print(curr)
                if curr.find(l_name) == -1:
                    pass
                else:
                    results.append(i)
    
        return results

    def get_centres_by_service(self, service):
        if len(self._centre_list) != 0:
            matches = []
            for i in self._centre_list:
                centre_services = i.get_services()
                for c_serv in centre_services:
                    if service == c_serv:
                        matches.append(i)
        
            if len(matches) == 0:
                return False
            else:
                return matches
        else:
            return False
        
    def get_centre_by_location(self, location):
        if len(self._centre_list) != 0:
            matches = []
            for i in self._centre_list:
                string_loc = i.get_location().lower()
                if  string_loc.find(location):
                    matches.append(i)
            return matches
        else:
            return False

    def get_centres_by_suburb(self, suburb):
        if len(self._centre_list) != 0:
            matches = []
            for i in self._centre_list:
                location = i.get_location()
                centre_suburb = location.get_suburb().lower()
                if  suburb.lower() == centre_suburb:
                    matches.append(i)
            if len(matches) == 0:
                return False
            else:
                return matches
        else:
            return False

