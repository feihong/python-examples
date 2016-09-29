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
        'value': 0.3
    }
)

sender = dict(
    contact_name='Hugo Strongola',
    company_name=None,
    street1='126 Paddock Street',
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
    street1='400 State Street',
    city='Chicago',
    state='IL',
    postal_code='60605',
    country='USA',
    phone='1-403-504-4839',
    email='test@test.net',
    type='residential'
)

parcel = dict(
    box_type='custom',
    weight={
        'value': 0.3,
        'unit': 'lb'
    },
    dimension={
        'width': 1,
        'height': 4,
        'depth': 0.3,
        'unit': 'cm'
    },
    items=[
         item
    ]
)

payload = dict(
    is_document=False,
    async=False,
    shipper_accounts=[{'id': shipper_id}],
    shipment={
        'parcels': [parcel],
        'ship_from': sender,
        'ship_to': receiver,
    }
)

try:
    api = Postmen(api_key, region)
    result = api.create('rates', payload)
    for rate in result['rates']:
        print(rate['service_type'], rate['total_charge']['amount'])
except PostmenException as ex:
    print(ex.code())
    print(ex.message())
    print(ex.details())
