from datetime import timedelta, datetime, date
from ics import Calendar, Event
import json
# import requests

# url = 'https://apis.digital.gob.cl/fl/feriados/2020'      # api with every holiday in Chile
# response = requests.get(url)      # not working, don't know why

with open('2020_Holidays.json') as f:
    file = json.load(f)
holiday_list = [datetime.strptime(day['fecha'],'%Y-%m-%d').date() for day in file]


# Make it a class?
class IcsGenerator:
    def __init__(self, name, start, end, days, start_time, duration, details="", json_file="2020_Holidays.json"):
        self.c = Calendar()
        self.event_name = name
        self.starting_date = start  # should be datetime object
        self.ending_date = end  # should be datetime object
        self.days_of_week = days  # list with the days of the week
        self.starting_time = start_time  # should be datetime object
        self.duration = duration  # datetime object (use as timedelta)
        self.details = details      # extra stuff, optional
        with open(json_file) as f:
            file = json.load(f)
        self.holiday_list = [datetime.strptime(day['fecha'], '%Y-%m-%d').date() for day in file]

    def generate_event(self, event_date):
        e = Event()
        e.name = self.event_name
        e.begin = event_date
        dur = [int(t) for t in self.duration.split(":")]
        e.duration = timedelta(hours=dur[0], minutes=dur[1])
        e.description = self.details
        return e

    # Since Python ICS doesn't support the repeat command, we can make a list of every date we need
    def get_dates(self):
        """Gets every date when the event takes place, excludes holidays"""
        event_days = []
        begining_day = datetime.strptime(self.starting_date + self.starting_time, '%Y-%m-%d%H:%M')
        final_day = datetime.strptime(self.ending_date + '23:59', '%Y-%m-%d%H:%M')
        day_index = begining_day
        while day_index < final_day:
            if day_index.date() not in holiday_list and day_index.weekday() in self.days_of_week:
                event_days.append(day_index)
            day_index += timedelta(days=1)
        return event_days

    def add_to_calendar(self):
        for event_day in self.get_dates():
            self.c.events.add(self.generate_event(event_day))


a = "12-04-2020"
t = "14:21"
dt = datetime.strptime(a + t, '%d-%m-%Y%H:%M')
dt2 = datetime.strptime(a, '%d-%m-%Y')
dt3 = dt
dt3 += timedelta(days=20)
dt4 = dt
print(a)
print(t)
print(dt)
print(dt2)
print(dt3)
print(dt.weekday())
days = [1, 3, 4]
lista = []
while dt4 < dt3:
    if dt4.weekday() in days:
        lista.append(dt4)
    dt4 += timedelta(days=1)

for i in lista:
    print(i.weekday(), i, i.date() in holiday_list)

print("---------------")

for i in holiday_list:
    print(i)