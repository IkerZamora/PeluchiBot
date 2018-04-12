from datetime import datetime
import json
import pytz

class Event:
	
	def __init__(self, acronym, date, first_edition_year, name):
		self.acronym = acronym
		self.date = date
		self.first_edition_year = first_edition_year
		self.name = name
		self.edition = self.date.year - self.first_edition_year + 1

	def time_left(self):
		'''
		Return: days, hours, minutes and seconds
		        remaining for the next LAN party
		'''
		now = datetime.now(tzinfo=pytz.timezone('Europe/Madrid'))
		td = self.date - now
		days = td.days
		hours = td.seconds // 3600
		minutes = (td.seconds // 60) % 60
		seconds = (td.seconds % 3600) % 60
		return days, hours, minutes, seconds

class Events:

	def __init__(self):
		self.events = []

	def _load_events(self, filename = 'events.json'):
		file = open(filename)
		data = json.load(file)
		file.close()
		json_events = data['events']
		for event in json_events:
			current = event['event']
			year = current['date']['year']
			month = current['date']['month']
			day = current['date']['day']
			hour = current['date']['hour']
			minute = current['date']['minute']
			date = datetime(year,month,day,hour,minute)
			date.replace(tzinfo=pytz.timezone('Europe/Madrid'))
			current_event = Event(current['acronym'], date, current['first_edition_year'], current['name'])
			self.events.append(current_event)

	def get_event(self, acronym):
		self._load_events()
		for event in self.events:
			if event.acronym.lower() == acronym.lower():
				return event
		return 0