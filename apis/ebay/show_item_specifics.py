import json
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {
    'ItemID': 181926350758,
    'IncludeItemSpecifics': True,
    'OutputSelector': [
        'Item.ItemSpecifics.NameValueList',
        'Item.ShippingPackageDetails',
    ]
})
# with open('item.json', 'w') as fp:
#     json.dump(response.dict(), fp, indent=2)

item = response.reply.Item

spd = item.ShippingPackageDetails
print('{} lb, {} oz'.format(spd.WeightMajor.value, spd.WeightMinor.value))

item_specifics = item.ItemSpecifics.NameValueList
for spec in item_specifics:
    print('- %s: %s' % (spec.Name, spec.Value))
