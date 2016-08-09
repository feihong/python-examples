"""
To successfully run this script, the user associated with the credentials must
be granted the appropriate permissions. For example, in IAM, go to the user's
Permissions tab and attach the AmazonSNSFullAccess policy.

"""

from pprint import pprint
import os
import datetime
import boto3


access_key, secret_key = os.environ['AWS_PARAMS'].split(';')


client = boto3.client(
    'sns',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

now = datetime.datetime.now()

resp = client.publish(
    PhoneNumber=os.environ['SMS_NUMBER'],
    Message='This message was sent via the API on {:%I:%M}'.format(now),
    MessageAttributes={
        'SMSType': {
            'StringValue': 'Promotional',
            'DataType': 'String',
        }
    }
)
pprint(resp)
