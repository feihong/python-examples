import json
from pprint import pprint
import os

import arrow

from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

# with open('request.xml', 'w') as fp:
#     xml = api.build_request_data('ReviseItem', {
#         'Item': {
#             'ItemID': '171992581865',
#             'PrimaryCategory': {
#                 'CategoryID': '49888950013',
#             },
#             'SecondaryCategory': {
#                 'CategoryID': '49889010013',
#             }
#         }
#     }, None)
#     fp.write(xml)

try:
    response = api.execute('ReviseItem', {
        'Item': {
            'ItemID': '171992581865',
            'PrimaryCategory': {
                'CategoryID': '49888950013',
            },
            'SecondaryCategory': {
                'CategoryID': '49889010013',
            }
        }
    })
    pprint(response.dict())
except ConnectionError as ce:
    pprint(ce.response.dict())
