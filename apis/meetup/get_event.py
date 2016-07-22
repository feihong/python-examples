"""
The /:urlname/events/:event_id/ endpoint does not actually contain RSVP data.

"""
import json
import os
from urllib.parse import urlencode
import requests
import arrow


url = 'https://api.meetup.com/chinese-11/events/232619194?key=' + os.environ['MEETUP_API_KEY']
event = requests.get(url).json()

with open('event.json', 'w') as fp:
    json.dump(event, fp, indent=2)

print(event['name'])
print(event['venue']['name'])
print(arrow.get(event['time'] / 1000.0).to('US/Central'))
print('RSVPs: %d' % event['yes_rsvp_count'])
print('Description:')
print(event['description'])
