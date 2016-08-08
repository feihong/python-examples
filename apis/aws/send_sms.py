"""
To successfully run this script, you must put the proper credentials in
~/.aws/credentials and give the user with those credentials the appropriate
permissions. For example, go to the user's Permissions tab in IAM and attach the
AmazonSNSFullAccess policy.

"""

from pprint import pprint
import os
import boto3

client = boto3.client('sns')

resp = client.publish(
    PhoneNumber=os.environ['SMS_NUMBER'],
    Message='This message was sent via the API',
    MessageAttributes={
        'SMSType': {
            'StringValue': 'Promotional',
            'DataType': 'String',
        }
    }
)
pprint(resp)
