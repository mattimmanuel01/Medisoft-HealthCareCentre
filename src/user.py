from flask_login import UserMixin

class User(UserMixin):
	'A class for storing all user data'
	def __init__(self,name,password,email,phone):
		self._name = name
		self._password = password
		self._email = email
		self._phone = phone
		self._authenticated = False

	# Setters
	def set_password(self,password):
		self._password = password

	# Getters
	def get_name(self):
		return self._name

	def get_password(self):
		return self._password
		
	def get_id(self):
		return self._email

	def get_phone(self):
		return self._phone

'''
	@property
	def is_authenticated(self):
		return self._authenticated 
	
	
	def authenticated(self, value):
		self._authenticated = value
'''
