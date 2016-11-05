"""
Get rates for 1 oz package using Shippo API.

Docs: https://goshippo.com/docs/reference

"""
import os
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


shipment = shippo.Shipment.create(
    object_purpose='QUOTE',
    address_from=address_from,
    address_to=address_to,
    parcel=parcel,
    async=False,
)

rates = shipment.rates_list
rates.sort(key=lambda x: float(x.amount))

for rate in rates:
    print('{} {}: {}'.format(rate.provider, rate.servicelevel_name, rate.amount))
