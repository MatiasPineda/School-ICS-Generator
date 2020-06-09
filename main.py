from datetime import timedelta, datetime, timezone
from ics import Calendar, Event
import json

# import requests

# url = 'https://apis.digital.gob.cl/fl/feriados/2020'      # api with every holiday in Chile
# response = requests.get(url)      # not working, don't know why

# todo: add url parameter to modify calendar as subscription. https://stackoverflow.com/questions/4239423/is-there-anyway-to-provide-a-ics-calendar-file-that-will-automatically-keep-in-s
# https://www.kanzaki.com/docs/ical/url.html
# I have to learn file hosting for that
# todo: once file can be hosted, add functions to change values of event
# todo: https://icalendar.org/validator.html#results


with open('2020_Holidays.json') as f:
    holiday_file = json.load(f)
holiday_list = [datetime.strptime(day['fecha'], '%Y-%m-%d').date() for day in holiday_file]
c = Calendar()
current_day_string = datetime.strftime(datetime.now(), '%Y-%m-%d')
current_time_string = datetime.strftime(datetime.now(), '%H:%M')


def fix_timezone_issue():
    """Returns difference between current time and UTC time to fix ICS Library UTC issue"""
    d = datetime.now(timezone.utc).astimezone()
    utc_offset = d.utcoffset() // timedelta(seconds=1)
    return utc_offset


def generate_event(event_name="New Event", event_date=datetime.now(), event_duration="1:00", event_description=""):
    """Generates event object using event elements as parameters"""
    e = Event()
    e.name = event_name
    e.begin = event_date
    dur = [int(t) for t in event_duration.split(":")]
    e.duration = timedelta(hours=dur[0], minutes=dur[1])
    e.description = event_description
    print(e)
    print('------')
    return e


def get_dates(starting_date=current_day_string, ending_date=current_day_string,
              starting_time="00:00", days_of_week=[], exclude_holidays=True):
    """Gets every date when the event takes place, excludes holidays. (exclude_holidays = False) to include holidays"""
    event_days = []
    first_day = datetime.strptime(starting_date + starting_time, '%Y-%m-%d%H:%M')
    last_day = datetime.strptime(ending_date + '23:59', '%Y-%m-%d%H:%M')
    # The next to lines have to be deleted if the ICS library fixes UTC issue
    first_day -= timedelta(seconds=fix_timezone_issue())
    last_day -= timedelta(seconds=fix_timezone_issue())
    day_index = first_day
    while day_index < last_day:
        if exclude_holidays:
            if day_index.date() not in holiday_list and day_index.weekday() in days_of_week:
                event_days.append(day_index)
        elif day_index.weekday() in days_of_week:
            event_days.append(day_index)
        day_index += timedelta(days=1)
    return event_days


def add_to_calendar(event_name="New Event", starting_date=current_day_string, ending_date=current_day_string,
                    days_of_week=[], starting_time="00:00", event_duration="1:00", event_description="",
                    exclude_holidays=True):
    """Generates and event for every day in get_dates function"""
    for event_day in get_dates(starting_date, ending_date, starting_time, days_of_week, exclude_holidays):
        c.events.add(generate_event(event_name, event_day, event_duration, event_description))


def create_ics_file():
    """Generates ICS file from calendar object"""
    with open('calendar.ics', 'w') as file:
        file.writelines(c)


def read_ics_file(ics_file='calendar.ics'):
    """Loads ics file, returns list of the ics file"""
    with open(ics_file, 'r') as file:
        ics_as_list = file.readlines()
    return ics_as_list


def identify_events(ics_file='calendar.ics'):
    """Formats list of events as a list of lists, separating each event on a new list"""
    ics_as_list = read_ics_file(ics_file)
    events_list = []
    event_begin = -1
    event_end = -1
    for index in range(len(ics_as_list)):
        if ics_as_list[index][0:6] == 'BEGIN:':
            event_begin = index
        if ics_as_list[index][0:4] == 'END:':
            event_end = index
        if event_begin != -1 and event_end != -1:
            events_list.append(ics_as_list[event_begin:event_end + 1])
            event_begin = -1
            event_end = -1
    # this part deletes the \n
    for event in events_list:
        for element in event:
            event[event.index(element)] = element[:-1]
    return events_list


def event_dictionary(ics_file='calendar.ics'):
    """Turn list of events as dictionary, returns a list of dictionaries"""
    event_list = identify_events(ics_file)
    dict_list = []
    for event in event_list:
        dictionary = {}
        for element in event:
            split = element.index(':')
            dictionary[element[:split]] = element[split + 1:]
        dict_list.append(dictionary)
    return dict_list


def check_if_event_in_ics(uid):
    """Returns tuple with bool as first element and a dict as second element"""
    for event in event_dictionary():
        if event.get('UID') == uid:
            return True, event
    return False, {}


def cancel_event(uid):
    """You can't cancel events from ics file, has to be manually,
     this moves selected event to now so you can delete it """
    event = list(check_if_event_in_ics(uid))
    time_now = datetime.now() - timedelta(seconds=(fix_timezone_issue()))
    formatted_time = datetime.strptime(time_now, '%Y%m%dT%H%m%S')
    if event[0]:
        event[1]['STATUS'] = 'CANCELLED'
        event[1]['DTSTART'] = str(formatted_time)


def change_duration(uid, new_duration='1:00'):
    event = list(check_if_event_in_ics())
    if event[0]:
        event[1]['DURATION'] = duration


def modify_events():
    uid_list = [event.get('UID') for event in event_dictionary()]
    return uid_list


name = "Maths"  # input("Name: ")
start = "2020-06-01"  # input("Start date yyyy-mm-dd")
end = "2020-06-14"  # input("End date yyyy-mm-dd")
days = [0, 2, 4]  # Monday, Wednesday, Friday
# while True:
#     d = (input("day of week (0-6)"))
#     if d == "" or int(d) < 0 or int(d) > 6:
#         break
#    days.append(int(d))
start_time = "18:50"  # input("Start time (hh:mm)")
duration = "1:20"  # input("Event duration (hh:mm)")
details = "Super boring"  # input("event description")
#
# generate = IcsGenerator(name, start, end, days, start_time, duration, details)
#
# generate.add_to_calendar()
# generate.create_ics_file()

new_start_time = '21:00'
new_duration = '2:00'

# add_to_calendar(name, start, end, days, start_time, duration, details)
# print(c)
# create_ics_file()
# print('---------------')
# print(fix_timezone_issue())

# print((read_ics_file()))
# print((read_ics_file())[3:-1])
# print(identify_events())
# print("."*20)
print(event_dictionary())
print("." * 20)
print(modify_events())

print("." * 20)
