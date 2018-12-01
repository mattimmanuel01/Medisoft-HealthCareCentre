
'''
(1) book an appointment (2) view a patient history 
(3) manage a patient history. The test-cases must be implemented with PyTest.
'''
class InvalidErrors(Exception):
	def __init__(self,errors):
		self._errors = errors

def check_login_input_fields(email,password):
	errors = {}
	try:
		if len(email) == 0 or len(password) == 0:
			raise InvalidErrors("Name or Email cannot be empty!")
	except InvalidErrors as a:
		errors['empty_field'] = a.errors

	try:
		if "@" not in email:
			raise InvalidErrors("Invalid Email Address")
	except InvalidErrors as b:
		errors['invalid_email'] = b.errors

	return errors


