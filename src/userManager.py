from src.user import *
from src.patient import *
from src.healthProvider import *


class UserManager:
    #Class in charge of keeping a list of all users and performing relevant methods
    def __init__(self):
        self._patients = []
        self._providers = []
    
    # Setters
    def add_patient(self, name, password, email, phone, medicare):
        patient = Patient(name, password, email, phone, medicare)
        self._patients.append(patient)

    def add_provider(self, name, password, email, phone, provider_num, profession):
        provider = HealthProvider(name, password, email, phone, provider_num, profession)
        self._providers.append(provider)

    # Getters
    def verify_user(self, email, password):
        for i in self._patients:
            if email.lower() == i.get_id().lower():
                if password == i.get_password():
                    return True
        for i in self._providers:
            if email.lower() == i.get_id().lower():
                if password == i.get_password():
                    return True
        return False
    
    #returns list
    def get_patients(self):
        return self._patients
    
    def get_providers(self):
        return self._providers
    
    #returns object
    def get_patient(self, email):
        if len(self._patients) != 0:
            for i in self._patients:
                if email.lower() == i.get_id().lower():
                    return i
        else:
            return False

    #returns object
    def get_provider(self, email):
        if len(self._providers) != 0:
            for i in self._providers:
                if email.lower() == i.get_id().lower():
                    #print("name - ");
                    return i
        else:
            #print("provider length is 0)l
            return False
    #list
    def get_providers_by_service(self, service):
        if len(self._providers) != 0:
            matches = []
            for i in self._providers:
                if service.lower() == i.get_profession().lower():
                    matches.append(i)
            if len(matches) == 0:
                return False
            else:
                return matches
        else:
            return False
                
	#list of partial matches to name
    def get_providers_part_name(self, name):
        results = []
        if len(self._providers) != 0:
            l_name = name.lower()
            for i in self._providers:
                curr = i.get_name().lower()
                print(curr)
                if curr.find(l_name) == -1:
                    pass
                else:
                    results.append(i)

        return results

    def get_providers_by_name(self, name):
        if len(self._providers) != 0:
            matches = []
            for i in self._providers:
                if name.lower() == i.get_name().lower():
                    matches.append(i)
            if len(matches) == 0:
                return False
            else:				
                return matches
        else:
            return False

    def is_provider(self, email, password):
        for i in self._providers:
            if email.lower() == i.get_id().lower():
                if password == i.get_password():
                    return True
                    
        return False


'''
UM = UserManager()
UM.add_patient("bob","bob","bob","bob","bob")
UM.add_provider("gus", "gus", "gus", "gus", "gus", "gus")
UM.add_provider("bus", "bus", "bus", "gus", "gus", "gus")

lol = UM.get_providers_by_name("i")
print(len(lol))
for i in lol:
	print(i._name)
#for i in lol:
#	print(i)

print(UM.verify_user("bob","bob"))
'''

