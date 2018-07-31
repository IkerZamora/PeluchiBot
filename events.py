from bs4 import BeautifulSoup
import calendar
from datetime import datetime, timedelta
import json
import locale
import logging
import requests
import requests_cache

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

class Event:
    
    def __init__(self, acronym, date, first_edition_year, name, url):
        self.logger = logging.getLogger(__name__)
        self.acronym = acronym
        self.date = date
        self.first_edition_year = first_edition_year
        self.name = name
        self.edition = self.date.year - self.first_edition_year + 1
        self.url = url

    def time_left(self):
        '''
        Return: days, hours, minutes and seconds
                remaining for the next LAN party
        '''
        now = datetime.now()
        td = self.date - now
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds // 60) % 60
        seconds = (td.seconds % 3600) % 60
        return days, hours, minutes, seconds

    def update_date(self):
        response = requests.get(self.url)
        if response.from_cache:
            self.logger.info(
                'Loading request for %s event from cache.' % self.name
            )
        else:
            self.logger.info(
                'Caching request for %s event to cache.' % self.name
            )
        if response.history:
            url_edition = int(response.url.split('.')[0]
                .replace('https://', '').replace(self.acronym.lower(), '')
            )
            if url_edition == self.edition + 1:
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    # str e.g: Del 26 al 29 de julio de 2018
                    str_date = (soup.find('a', {'name': 'cuando'})
                        .parent.findNext('p').text.lower().split()
                    )
                    # pre-event day is the previous day to the official start.
                    start_day = int(str_date[1]) - 1
                    end_day = int(str_date[3])
                    month = None
                    for value, key in enumerate(calendar.month_name):
                        if key == str_date[5]:
                            month = value
                    year = int(str_date[7])
                    date = datetime(
                        year,
                        month,
                        start_day,
                        self.date.hour,
                        self.date.minute
                    )
                    self.date = date
                except:
                    self.logger.exception()
            else:
                self.logger.info(
                    'URL for edition {} of {} event has not been updated yet.'
                    .format(self.edition + 1, self.name)
                )
        else:
            self.logger.error('URL redirection of %s event did not happen.'
                % self.name)
        return self

class Events:

    CACHE_EXPIRE = 3600

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        requests_cache.install_cache(
            cache_name='date_cache',
            backend='memory',
            expire_after=Events.CACHE_EXPIRE
        )
        self.logger.info('Initialized in-memory cache for event date updater ' 
            + 'with expiration set for %d minutes.' % (Events.CACHE_EXPIRE / 60)
        )
        self.events = self._load_events()

    def _load_events(self, filename = 'events.json'):
        file = open(filename)
        data = json.load(file)
        file.close()
        json_events = data['events']
        now = datetime.now()
        events = []
        for event in json_events:
            current = event['event']
            url = current['url']
            year = current['date']['year']
            month = current['date']['month']
            day = current['date']['day']
            hour = current['date']['hour']
            minute = current['date']['minute']
            date = datetime(year,month,day,hour,minute)
            current_event = Event(
                current['acronym'],
                date,
                current['first_edition_year'],
                current['name'],
                url
            )
            if date < now:
                current_event = current_event.update_date()
            events.append(current_event)
        return events

    def get_event(self, acronym):
        for event in self.events:
            if event.acronym.lower() == acronym.lower():
                return event
        return None

    def set_event(self, acronym, set_event):
        for index, event in enumerate(self.events):
            if event.acronym.lower() == acronym.lower():
                self.events[index] = set_event

    def next_event(self):
        now = datetime.now()
        # Since events occur annually max. time-lapse is 1 year.
        soonest_date = now + timedelta(days=366) # Using Leap year just in case.
        next_event = None
        for event in self.events:
            if event.date > now and event.date < soonest_date:
                next_event = event
                soonest_date = event.date
        return next_event