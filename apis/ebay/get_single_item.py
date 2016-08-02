import json
from pprint import pprint
import os
from ebaysdk.shopping import Connection as Shopping


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Shopping(config_file=None, **credentials)

response = api.execute('GetSingleItem', {
    'ItemID': 171992581889,
    'IncludeSelector': 'ItemSpecifics',
    # 'IncludeSelector': 'Details',     # will not include ItemSpecifics field
})
with open('item.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

item = response.reply.Item
item_specifics = item.ItemSpecifics.NameValueList
print('Title: ' + item.Title)
print('Item specifics:')
for spec in item_specifics:
    print('- %s: %s' % (spec.Name, spec.Value))
