import json
from pprint import pprint
import os

import arrow

from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

now = arrow.utcnow()
later = now.replace(days=+120)

def get_page(page):
    response = api.execute('GetSellerList', {
        'EndTimeFrom': now,
        'EndTimeTo': later,
        'GranularityLevel': 'Coarse',
        'OutputSelector': [
            'ReturnedItemCountActual',
            'PaginationResult',
            'ItemArray.Item.ItemID',
            'ItemArray.Item.Title',
            'ItemArray.Item.Storefront',
        ],
        'Pagination': {
            'EntriesPerPage': 200,
            'PageNumber': page,
        },
    })
    return response.dict()


def get_all_items():
    page = get_page(1)
    yield from page['ItemArray']['Item']
    page_count = int(page['PaginationResult']['TotalNumberOfPages'])
    for i in range(1, page_count):
        page = get_page(i)
        yield from page['ItemArray']['Item']


with open('item_categories.json', 'w') as fp:
    items = list(get_all_items())
    json.dump(items, fp, indent=2)
