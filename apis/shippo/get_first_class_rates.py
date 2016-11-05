"""
Print out a table of first class rates using Shippo API.

Docs: https://goshippo.com/docs/reference

Shippo's first class rates are on par with those of EasyPost, but they charge 5
cents per label:

https://goshippo.com/pricing/

"""
import os
from requests.packages import urllib3
urllib3.disable_warnings()
import shippo


shippo.api_key = os.environ['SHIPPO_API_KEY']

weights = list(range(1, 16)) + [15.9]

address_from = {
    'object_purpose': 'QUOTE',
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
    'object_purpose': 'QUOTE',
    'name': 'Mr. Hippo',
    'street1': '1092 Indian Summer Ct',
    'city': 'San Jose',
    'state': 'CA',
    'zip': '95122',
    'country': 'US',
    'phone': '+1 555 341 9393',
    'email': 'mrhippo@goshippo.com'
}


for weight in weights:
    parcel = {
        'length': 5,
        'width': 5,
        'height': 2,
        'distance_unit': 'in',
        'weight': weight,
        'mass_unit': 'oz',
    }

    shipment = shippo.Shipment.create(
        object_purpose='QUOTE',
        address_from=address_from,
        address_to=address_to,
        parcel=parcel,
        async=False,
    )

    rate = min(shipment.rates_list, key=lambda x: float(x.amount))
    print('{} oz: {}'.format(weight, rate.amount))
