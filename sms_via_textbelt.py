import os
import datetime
import requests


result = requests.post('http://textbelt.com/text', dict(
    number=os.environ['SMS_TARGET'],
    message='This message was sent at %s' % datetime.datetime.now(),
)).json()

if result['success'] == True:
    print('Message successfully sent!')
else:
    print('Message sending failed: %s' % result['message'])
