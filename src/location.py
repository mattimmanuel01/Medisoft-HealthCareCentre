
class Location:
	def __init__(self, suburb,city=None,state=None,street=None,streetnum=None):
		self._suburb = suburb
		self._city = city
		self._state = state
		self._street = street
		self._streetnum = streetnum
		self._location = suburb +(", " + city if city else "")+(", " + state if state else "")+(", " + street if street else "")+(", " + streetnum if streetnum else "")

	def get_suburb(self):
		return self._suburb

	def __str__(self):
		return self._location
