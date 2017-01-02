"""
There is no endpoint specifically for fetching a single order. You must use
GetOrders and pass it a single order ID.

Order URLs look like this:

http://k2b-bulk.ebay.com/ws/eBayISAPI.dll?EditSalesRecord&transid=1351863146004&urlstack=5508|Period_Last90Days|currentpage_SCSold|&itemid=141543584879

You can extract the order ID by this formula:

{itemid}-{transid}
"""
import json
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))

api = Trading(config_file=None, **credentials)
response = api.execute('GetOrders', {
    'OrderIDArray': [
        {'OrderID': '141543584879-1351863146004'}
    ]
})
with open('order.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

rdict = response.dict()
orders = rdict['OrderArray']['Order']
order = orders[0]
text = json.dumps(order['ShippingAddress'], indent=2)
print(text)

transactions = order['TransactionArray']['Transaction']
for transaction in transactions:
    tracking_details = transaction['ShippingDetails']['ShipmentTrackingDetails']
    print(tracking_details)
