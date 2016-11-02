"""
Print out a table of first class rates for 1-16 oz.

"""
import os
import json
import requests


api_key = os.environ['SHIPHAWK_API_KEY']

url = 'https://sandbox.shiphawk.com/api/v4/rates?api_key=' + api_key

weights = list(range(1, 16)) + [15.9]


for weight in weights:
    data = {
      'items':[
        {
          'item_type': 'parcel',
          'length': 6,
          'width' : 7,
          'height': 1,
          'weight': weight,
          'value': 15.00
        }
      ],
      'origin_address':{ 'zip': '93101'},
      'destination_address':{ 'zip': '60060'}
    }
    response = requests.post(url, json.dumps(data))
    fc_rate = [rate for rate in response.json()['rates']
               if rate['service_level'] == 'First-Class Mail'][0]
    print('{} oz: {:.2f}'.format(weight, fc_rate['price']))
