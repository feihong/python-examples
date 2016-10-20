"""
There is no endpoint specifically for fetching a single order. You must use
GetOrders and pass it a single order ID.

"""
import json
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))

api = Trading(config_file=None, **credentials)
response = api.execute('GetOrders', {
    'OrderIDArray': [
        {'OrderID': '172074247204-1606470485007'}
    ]
})
with open('order.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

rdict = response.dict()
orders = rdict['OrderArray']['Order']
text = json.dumps(orders[0]['ShippingAddress'], indent=2)
print(text)
