from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {'ItemID': 181926350758})
# pprint(response.dict())
details = response.reply.Item.ShippingPackageDetails
print(details)

lb = int(details.WeightMajor.value)
oz = int(details.WeightMinor.value)

print('Item weights %d oz' % (16 * lb + oz))
