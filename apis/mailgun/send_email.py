"""
API reference:
https://documentation.mailgun.com/api_reference.html

According to the pricing page, your first 10k messages per month are free:
http://www.mailgun.com/pricing

"""
import sys
import os
import datetime
from pprint import pprint
import requests


recipient = sys.argv[1]

domain, private_key = os.environ['MAILGUN_PARAMS'].split(';')

url = 'https://api.mailgun.net/v3/{domain}/messages'.format(domain=domain)

resp = requests.post(
    url,
    auth=('api', private_key),
    data={
        'from': 'Overlord <overlord@{}>'.format(domain),
        'to': recipient,
        'subject': 'Hello from Mailgun',
        'text': 'This email was sent at {:%I:%M}'.format(datetime.datetime.now()),
    },
)
pprint(resp.text)
