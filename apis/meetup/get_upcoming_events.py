import json
import os
from urllib.parse import urlencode
import requests
import arrow


api_key = os.environ['MEETUP_API_KEY']


url = 'https://api.meetup.com/chinese-11/events?status=upcoming&key=' + api_key
events = requests.get(url).json()

# with open('events.json', 'w') as fp:
#     json.dump(events, fp, indent=2)

for event in events:
    print(event['id'])
    print(event['name'])
    dt = arrow.get(event['time'] / 1000.0).to('US/Central')
    print(dt)
    print('RSVP count: %d' % event['yes_rsvp_count'])
    print('Venue: ' + event['venue']['name'])
    print('='*80)
