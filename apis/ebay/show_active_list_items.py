from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetMyeBaySelling', {
    'ActiveList': {
        'Include': True
    }
})
# pprint(response.dict())
items = response.reply.ActiveList.ItemArray.Item
print('Got %d active list items\n' % len(items))

print('First item:')
item = items[0]
print(item.Title)
print(item.ListingDetails.ViewItemURL)
print(item.BuyItNowPrice.value)
