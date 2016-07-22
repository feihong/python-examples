import json
import os
from urllib.parse import urlencode
import requests
import arrow


url = 'https://api.meetup.com/chinese-11/events/232619194/rsvps?key=' + os.environ['MEETUP_API_KEY']
rsvps = requests.get(url).json()

# with open('rsvps.json', 'w') as fp:
#     json.dump(rsvps, fp, indent=2)

for rsvp in rsvps:
    print(rsvp['member']['id'])
    print(rsvp['member']['name'])
    print('Response: ' + rsvp['response'])
    print('='*80)
