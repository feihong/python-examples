"""
Download the category structure for the given store.

"""
import json
import os
from pprint import pprint
from ebaysdk.trading import Connection as Trading


ITEM_ID = '142026412435'


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetStore', {
    'CategoryStructureOnly': True,
})
pprint(response.dict())
