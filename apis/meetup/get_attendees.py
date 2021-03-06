"""
The endpoint used in this example only works with events that have already
started. If you try to use it on an event that hasn't yet started yet, you'll
get an error:

    "errors": [
        {
          "message": "Event must have started",
          "code": "event_time_error"
        }
    ]

"""

import json
import os
from urllib.parse import urlencode
import requests
import arrow


EVENT_ID = '232062583'


def get_attendance(filter):
    url = 'https://api.meetup.com/chinese-11/events/%s/attendance?filter=%s&key=%s' % (
        EVENT_ID, filter, os.environ['MEETUP_API_KEY'])
    return requests.get(url).json()

# with open('attendance.json', 'w') as fp:
#     json.dump(items, fp, indent=2)

print('Attended:')
for item in get_attendance('attended'):
    print('- ' + item['member']['name'])

print('\nExcused:')
for item in get_attendance('excused'):
    print('- ' + item['member']['name'])

print('\nNo show:')
for item in get_attendance('noshow'):
    print('- ' + item['member']['name'])
