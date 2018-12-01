from healthCareCentre import *
import time
import datetime as dt

class WorkPlace():
	'stores the centre and respective hours worked at it'	
	def __init__(self, HealthCareCentre, start, end):
		self._centre = HealthCareCentre
		self._start = Hours(start)
		self._end = Hours(end)
		self._roster = []


	def get_start_hours(self):
		return self._start.get_time()

	def get_end_hours(self):
		return self._end.get_time()

	def get_centre_name(self):
		return self._centre.get_name()

	def get_roster(self):
		return self._roster

	def add_time_slot(self, atime):
		time_slot = TimeSlot(atime)
		self._roster.append(time_slot)


class Hours():
	def __init__(self,time):
		time_format = '%H:%M'
		self._time = dt.datetime.strptime(str(time), time_format)
		self._zero = dt.datetime.strptime('00:00', '%H:%M')
		self._thirty = dt.datetime.strptime('00:30', '%H:%M')

	def get_time(self):
		return self._time

	def add_time(self):
		return (self._time - self._zero + self._thirty).time()


class TimeSlot():
	def __init__(self, atime):
		self._time = atime

	def get_time(self):
		return self._time
	
	


