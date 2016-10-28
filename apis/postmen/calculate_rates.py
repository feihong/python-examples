"""
Source: https://github.com/postmen/postmen-sdk-python/blob/master/examples/rates_create.py

2016 USPS Rate Chart:
https://www.postmen.com/courier/usps/rates/

What values are allowed for box_type:
https://docs.postmen.com/usps.html#parcel

"""
import json
import os
from postmen import Postmen, PostmenException


api_key, shipper_id = os.environ['POSTMEN_PARAMS'].split(';')
region = 'sandbox'

# In ounces
weights = [1, 2, 3, 4, 5]


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

# box_type = 'custom'
box_type = 'usps_parcel'
# box_type = 'usps_small_flat_rate_box'
# box_type = 'usps_flat_rate_envelope'
# box_type = 'usps_flat_rate_padded_envelope'

def get_payload(weight):
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
            'value': weight / 16,
        }
    )

    parcel = dict(
        box_type=box_type,
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
    return payload


print('Box type:', box_type)
print()

for weight in weights:
    print('Weight: {} oz'.format(weight))
    try:
        api = Postmen(api_key, region)
        result = api.create('rates', get_payload(weight))
        # with open('result.json', 'w') as fp:
        #     json.dump(result, fp, indent=2)
        for rate in result['rates']:
            print(rate['service_type'], rate['total_charge']['amount'])
        print('-'*75)
    except PostmenException as ex:
        print(ex.code())
        print(ex.message())
        print(ex.details())
