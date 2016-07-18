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
# with open('categories.json', 'w') as fp:
#     json.dump(response.dict()['Store']['CustomCategories']['CustomCategory'], fp, indent=2)

categories = response.reply.Store.CustomCategories.CustomCategory
for cat in categories:
    print(cat.Name)
    for child in getattr(cat, 'ChildCategory', []):
        print('- ' + child.Name)
        if hasattr(child, 'ChildCategory') and child.Name != '9 pc set':
            import ipdb; ipdb.set_trace()
