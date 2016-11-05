'''
Purchase a label using Shippo API.

Docs: https://goshippo.com/docs/reference

'''
import os
import webbrowser
from requests.packages import urllib3
urllib3.disable_warnings()
import shippo


shippo.api_key = os.environ['SHIPPO_API_KEY']

parcel = {
    'length': 5,
    'width': 5,
    'height': 2,
    'distance_unit': 'in',
    'weight': 1,
    'mass_unit': 'oz',
}

address_from = {
    'object_purpose': 'PURCHASE',
    'name': 'Mrs Hippo',
    'street1': '215 Clayton St.',
    'city': 'San Francisco',
    'state': 'CA',
    'zip': '94117',
    'country': 'US',
    'phone': '+1 555 341 9393',
    'email': 'laura@goshippo.com'
}

address_to = {
    'object_purpose': 'PURCHASE',
    'name': 'Mr. Hippo',
    'street1': '1092 Indian Summer Ct',
    'city': 'San Jose',
    'state': 'CA',
    'zip': '95122',
    'country': 'US',
    'phone': '+1 555 341 9393',
    'email': 'mrhippo@goshippo.com'
}


shipment = shippo.Shipment.create(
    object_purpose='PURCHASE',
    address_from=address_from,
    address_to=address_to,
    parcel=parcel,
    async=False,
)

rate = next(rate for rate in shipment.rates_list
            if rate.servicelevel_token == 'usps_first')

transaction = shippo.Transaction.create(
    rate=rate.object_id,
    label_file_type='PNG',
    async=False)

if transaction.object_status == 'SUCCESS':
    print('Tracking number %s' % transaction.tracking_number)
    url = transaction.label_url
    print('URL:', url)
    webbrowser.open(url)
else:
    print('Failed purchasing the label due to:')
    for message in transaction.messages:
        print('- %s' % message['text'])
