"""
Download the data for a given item as JSON.

"""
import json
import os
from pprint import pprint
from ebaysdk.trading import Connection as Trading


ITEM_ID = '172064937927'


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {
    'ItemID': ITEM_ID,
    'DetailLevel': 'ItemReturnDescription',
})
with open('item.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

print('Downloaded data for item %s to item.json' % ITEM_ID)
