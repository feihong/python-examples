import os
import requests


api_key = os.environ['SHIPHAWK_API_KEY']


url = 'https://sandbox.shiphawk.com/api/v4/rates?api_key=' + api_key

data = """{
  "items":[
    {
      "item_type": "parcel",
      "length": "10",
      "width" : "10",
      "height": "11",
      "weight": "10",
      "value": 100.00
    }
  ],
  "origin_address":{ "zip": "93101"},
  "destination_address":{ "zip": "60060"}
}"""
response = requests.post(url, data)
print(response.text)
