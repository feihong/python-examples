"""
Fetch orders given a datetime range. Retrieve all pages that match the
request criteria.

"""
import os
import datetime
import json
import itertools
import arrow
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)


def get_orders(start, end):
    for page in itertools.count(1):
        response = get_orders_for_page(page, start, end)
        reply = response.reply
        orders = response.dict()['OrderArray']['Order']
        for order in orders:
            yield order
        if reply.PageNumber == reply.PaginationResult.TotalNumberOfPages:
            break


def get_orders_for_page(page, start, end):
    response = api.execute('GetOrders', {
        'CreateTimeFrom': start,
        'CreateTimeTo': end,
        'OrderStatus': 'Completed',
    })
    pagination = response.reply.PaginationResult
    print('Page {} of {}: {} orders'.format(
        page,
        pagination.TotalNumberOfPages,
        response.reply.ReturnedOrderCountActual))
    return response


if __name__ == '__main__':
    start = arrow.get('2017-01-01')
    end = arrow.get('2017-01-02')

    print('Search range: {} to {}'.format(start, end))
    orders = list(get_orders(start, end))
    print('Got {} orders'.format(len(orders)))
    with open('orders.json', 'w') as fp:
        json.dump(orders, fp, indent=2)
