import json
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
trading = Trading(config_file=None, **credentials)

response = trading.execute('GetMyeBaySelling', {
    'ActiveList': {
        'Include': True
    },
    'OutputSelector': [
        'ActiveList.PaginationResult',
        'ActiveList.ItemArray.Item.Title',
        'ActiveList.ItemArray.Item.ItemID',
    ]
})

results = []
for item in response.reply.ActiveList.ItemArray.Item:
    results.append(dict(
        id=item.ItemID,
        title=item.Title,
    ))
with open('item_ids.json', 'w') as fp:
    json.dump(results, fp, indent=2)
