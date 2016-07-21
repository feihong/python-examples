import json
import datetime
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

with open('categories.json') as fp:
    categories = json.load(fp)

# with open('request.xml', 'w') as fp:
#     xml = api.build_request_data('SetStoreCategories', {
#         'Action': 'Add',
#         'StoreCategories': {
#             'CustomCategory': categories
#         }
#     }, None)
#     fp.write(xml)

response = api.execute('SetStoreCategories', {
    'Action': 'Add',
    'StoreCategories': {
        'CustomCategory': categories
    }
})
pprint(response.dict())
