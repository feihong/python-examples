import json
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetMyeBaySelling', {
    'ActiveList': {
        'Include': True
    },
    'OutputSelector': [
        'ActiveList.PaginationResult',
        'ActiveList.ItemArray.Item.Title',
        'ActiveList.ItemArray.Item.BuyItNowPrice',
        'ActiveList.ItemArray.Item.ListingDetails.ViewItemURL',        
    ]
})
with open('items.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)


items = response.reply.ActiveList.ItemArray.Item
print('Got %d active list items' % len(items))

pagination_result = response.reply.ActiveList.PaginationResult
print('%s total items' % pagination_result.TotalNumberOfEntries)
print('%s total pages' % pagination_result.TotalNumberOfPages)
print()

print('First item:')
item = items[0]
print(item.Title)
print(item.ListingDetails.ViewItemURL)
print(item.BuyItNowPrice.value)
