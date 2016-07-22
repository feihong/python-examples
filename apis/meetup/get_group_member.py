import json
import os
from urllib.parse import urlencode
import requests
import arrow


url = 'https://api.meetup.com/chinese-11/members/7616575?key=' + os.environ['MEETUP_API_KEY']
member = requests.get(url).json()

with open('member.json', 'w') as fp:
    json.dump(member, fp, indent=2)
