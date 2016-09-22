"""
See get_all_item_ids.py for getting a JSON file of item IDs and titles.
"""
import json
import os
from ebaysdk.shopping import Connection as Shopping


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
shopping = Shopping(config_file=None, **credentials)


def get_item(item_id):
    return shopping.execute('GetSingleItem', {
        'ItemID': item_id,
        'IncludeSelector': 'ItemSpecifics',
        # 'OutputSelector': '',
    })

with open('item_ids.json') as fp:
    item_dicts = json.load(fp)

model_dict = {}

for item_dict in item_dicts:
    item = get_item(item['item_id']).response.reply.Item
    model = [spec.Value for spec in Item.ItemSpecifics.NameValueList if spec.Name == 'Model']
    model = model[0]
    if model not in model_dict:
        model_dict[model = item_dict

model_list = list(model_dict.items())
model_list.sort(key=lambda x: x[0])
with open('item_models.txt', 'w') as fp:
    for model, item_dict in model_list:
        fp.write('{}\t{}\n'.format(model, item_dict['title']))
