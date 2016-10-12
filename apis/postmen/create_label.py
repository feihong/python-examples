"""
Source:
https://github.com/postmen/postmen-sdk-python/blob/master/examples/rates_create.py

"""
import json
import os
from postmen import Postmen, PostmenException


api_key, shipper_id = os.environ['POSTMEN_PARAMS'].split(';')
region = 'sandbox'


item = dict(
    description='Snack Bar',
    hs_code='11111111',
    origin_country='CHN',
    price={
        'amount': 13.50,
        'currency': 'USD'
    },
    quantity=1,
    sku='111-222-333',
    weight={
        'unit': 'lb',
        'value': 25
    }
)

sender = dict(
    contact_name='Hugo Strongola',
    company_name=None,
    street1='126 W Paddock Street',
    street2=None,
    street3=None,
    city='Crystal Lake',
    state='IL',
    postal_code='60014',
    country='USA',
    phone='1-403-504-5496',
    fax=None,
    fax_id=None,
    email='test@test.com',
    type='residential'
)

receiver = dict(
    contact_name='Magdalena Kumbata',
    street1='400 N State Street',
    street2=None,
    street3=None,
    city='Chicago',
    state='IL',
    postal_code='60602',
    country='USA',
    phone='1-403-504-4839',
    email='test@test.net',
    type='residential'
)

parcel = dict(
    box_type='usps_flat_rate_envelope',
    weight=item['weight'],
    dimension={
        'width': 7,
        'height': 5,
        'depth': 0.2,
        'unit': 'in'
    },
    items=[
         item
    ]
)


payload = {
    'async': False,
    'is_document': False,
    'return_shipment': False,
    'paper_size': 'default',
    'service_type': 'usps_priority_mail',
    'shipper_account': {
        'id': shipper_id,
    },
    'references': ['reference1', 'reference2'],
    'shipment': {
        'parcels': [parcel],
        'ship_from': sender,
        'ship_to': receiver
    }
}

try:
    api = Postmen(api_key, region)
    result = api.create('labels', payload)
    with open('result.json', 'w') as fp:
        json.dump(result, fp, indent=2)
except PostmenException as e:
    print(e.code())
    print(e.message())
    with open('error_details.json', 'w') as fp:
        json.dump(e.details(), fp, indent=2)
