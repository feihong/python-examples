"""
Source: https://github.com/postmen/postmen-sdk-python/blob/master/examples/rates_create.py

What values are allowed for box_type:
https://docs.postmen.com/usps.html#parcel

2016 USPS Rate Chart:
https://www.postmen.com/courier/usps/rates/

"""
import json
import os
from postmen import Postmen, PostmenException


api_key, shipper_id = os.environ['POSTMEN_PARAMS'].split(';')
region = 'sandbox'

# In ounces
# weights = [1, 2, 3, 4, 5]
weights = [1]


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

receiver = {
    'company_name': 'The Receiving Company',
    'contact_name': 'Recipient Name',
    'phone': '519-886-1310',
    'street1': '35 Albert St',
    'city': 'Waterloo',
    'state': 'ON',
    'postal_code': 'N2L 5E2',
    'country': 'CAN',
    'type': 'residential'
}

box_type = 'custom'
# box_type = 'usps_parcel'


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
            'width': 1,
            'height': 1,
            'depth': 0.2,
            'unit': 'in'
        },
        items=[item]
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
        payload = get_payload(weight)
        with open('payload.json', 'w') as fp:
            json.dump(payload, fp, indent=2)
        api = Postmen(api_key, region)
        result = api.create('rates', payload)
        with open('result.json', 'w') as fp:
            json.dump(result, fp, indent=2)
        for rate in result['rates']:
            print(rate['service_type'], rate['total_charge']['amount'])
        print('-'*75)
    except PostmenException as ex:
        print(ex.code())
        print(ex.message())
        print(ex.details())
