import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


app_id = os.environ['EBAY_PARAMS'].split(';')[0]
api = Connection(appid=app_id, config_file=None)
response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

print(response.reply.ack)
items = response.reply.searchResult.item
print('Number of items: %d' % len(items))
item = items[0]
print('First item: %s\n' % item.title)
print(item)
