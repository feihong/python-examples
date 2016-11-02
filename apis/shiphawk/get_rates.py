import os
import json
import requests


api_key = os.environ['SHIPHAWK_API_KEY']


url = 'https://sandbox.shiphawk.com/api/v4/rates?api_key=' + api_key

data = {
  'items':[
    {
      'item_type': 'parcel',
      'length': '5',
      'width' : '5',
      'height': '2',
      'weight': '1',
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
