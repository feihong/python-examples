import json
from pprint import pprint
import os

import arrow

from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

now = arrow.utcnow()
later = now.replace(days=+120)

response = api.execute('GetSellerList', {
    'EndTimeFrom': now,
    'EndTimeTo': later,
    'GranularityLevel': 'Medium',
    'Pagination': {
        'EntriesPerPage': 10,
    },
    'OutputSelector': [
        'ReturnedItemCountActual',
        'PaginationResult',
        'ItemArray.Item.ItemID',
        'ItemArray.Item.Title',
        'ItemArray.Item.Storefront',
    ]
})
with open('items.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)
