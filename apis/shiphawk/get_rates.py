"""
Get rates from ShipHawk API.

The rates seem identical to those for EasyPost.

"""
import os
import json
import requests


api_key = os.environ['SHIPHAWK_API_KEY']


url = 'https://sandbox.shiphawk.com/api/v4/rates?api_key=' + api_key

data = {
  'items':[
    {
      'item_type': 'parcel',
      'length': 6,      # in inches
      'width' : 7,
      'height': 1,
      'weight': 2,      # in ounces
      'value': 15.00
    }
  ],
  'origin_address':{ 'zip': '93101'},
  'destination_address':{ 'zip': '60060'}
}
response = requests.post(url, json.dumps(data))
# print(json.dumps(response.json(), indent=2))
for rate in response.json()['rates']:
    print('{carrier} {service_level}: {price}'.format(**rate))
