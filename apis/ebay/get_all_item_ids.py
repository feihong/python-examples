import itertools
import json
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
trading = Trading(config_file=None, **credentials)


def get_page(page_num):
    return trading.execute('GetMyeBaySelling', {
        'ActiveList': {
            'Include': True,
            'Pagination': {
                'PageNumber': page_num
            }
        },
        'OutputSelector': [
            'ActiveList.PaginationResult',
            'ActiveList.ItemArray.Item.Title',
            'ActiveList.ItemArray.Item.ItemID',
        ]
    })


def get_items():
    for page_num in itertools.count(1):
        print('Page %s' % page_num)
        response = get_page(page_num)
        active = response.reply.ActiveList
        page_count = int(active.PaginationResult.TotalNumberOfPages)
        yield from active.ItemArray.Item
        if page_count == page_num:
            break


item_dicts = list(
    dict(id=item.ItemID, title=item.Title) for item in get_items()
)
print('Item count: %d' % len(item_dicts))
with open('item_ids.json', 'w') as fp:
    json.dump(item_dicts, fp, indent=2)
