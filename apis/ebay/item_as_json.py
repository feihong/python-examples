"""
Download the data for a given item as JSON.

"""
import json
import os
from pprint import pprint
from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping


ITEM_ID = '141991824219'


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))

trading = Trading(config_file=None, **credentials)
response = trading.execute('GetItem', {
    'ItemID': ITEM_ID,
    'DetailLevel': 'ReturnAll',
    # 'DetailLevel': 'ItemReturnAttributes',  # to get UPC
})
item = response.dict()

shopping = Shopping(config_file=None, **credentials)
response = shopping.execute('GetSingleItem', {
    'ItemID': ITEM_ID,
    'IncludeSelector': 'ItemSpecifics'
})
item['Item']['ItemSpecifics'] = response.dict()['Item']['ItemSpecifics']

with open('item.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

print('Downloaded data for item %s to item.json' % ITEM_ID)
