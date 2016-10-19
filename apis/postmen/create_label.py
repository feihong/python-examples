"""
Source:
https://github.com/postmen/postmen-sdk-python/blob/master/examples/labels_create.py

API page:
https://docs.postmen.com/usps.html#labels-create-a-label

"""
import json
import os
import webbrowser
from postmen import Postmen, PostmenException


api_key, shipper_id = os.environ['POSTMEN_PARAMS'].split(';')
region = 'sandbox'


sender = {
    'city': 'Chicago',
    'contact_name': 'Poppy Luffy Esq.',
    'country': 'USA',
    'phone': '312-744-7616',
    'postal_code': '60625',
    'state': 'IL',
    'street1': '4455 N. Lincoln Ave.',
    'type': 'residential'
}

receiver = {
    'city': 'Crystal Lake',
    'company_name': 'The Receiving Company',
    'contact_name': 'Recipient Name',
    'country': 'USA',
    'phone': '302-0123-1234',
    'postal_code': '60014',
    'state': 'IL',
    'street1': '126 W Paddock St,',
    'street2': 'Wow Avenue',
    'street3': 'Boring part of town',
    'type': 'residential'
}

parcel = {
    'box_type': 'custom',
    'description': 'Food XS',
    'dimension': {
        'depth': 3,
        'height': 5,
        'width': 4,
        'unit': 'in',
    },
    'weight': {'value': 0.6, 'unit': 'lb'},
    'items': [
        {
            'description': 'Food Bar',
            'origin_country': 'USA',
            'price': {'amount': 3, 'currency': 'USD'},
            'quantity': 2,
            'sku': 'Epic_Food_Bar',
            'weight': {'value': 0.3, 'unit': 'lb'},
        }
    ],
}

payload = {
    'async': False,
    'is_document': False,
    'paper_size': 'default',
    'return_shipment': False,
    'service_type': 'usps_first_class_mail',
    'shipper_account': {'id': shipper_id},
    'references': ['reference1', 'reference2', 'reference3'],
    'shipment': {
        'parcels': [parcel],
        'ship_from': sender,
        'ship_to': receiver,
    },
}

try:
    api = Postmen(api_key, region)
    result = api.create('labels', payload)
    url = result['files']['label']['url']
    webbrowser.open(url)
    # with open('result.json', 'w') as fp:
    #     json.dump(result, fp, indent=2)
    print('Cost: {}'.format(result['rate']['total_charge']['amount']))
    print('Tracking number: {}'.format(result['tracking_numbers'][0]))
except PostmenException as e:
    print(e.code())
    print(e.message())
    with open('error_details.json', 'w') as fp:
        json.dump(e.details(), fp, indent=2)
