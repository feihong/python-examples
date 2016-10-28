"""
Fetch historical orders based on a datetime range, but exclude most fields in
the response.

"""
import os
import datetime
import json
import itertools
import arrow
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

start = arrow.utcnow().replace(days=-120).replace(
    hour=0, minute=0, second=0, microsecond=0)
end = start.replace(days=+20)

def get_orders(page):
    response = api.execute('GetOrders', {
        'CreateTimeFrom': start,
        'CreateTimeTo': end,
        'OrderStatus': 'Completed',
        'SortingOrder': 'Ascending',
        'Pagination': {
            'PageNumber': page,
            'EntriesPerPage': 100,
        },
        'OutputSelector': [
            'PageNumber',
            'PaginationResult',
            'ReturnedOrderCountActual',
            'OrderArray.Order.TransactionArray.Transaction.Item.ItemID',
            'OrderArray.Order.TransactionArray.Transaction.QuantityPurchased',
            'OrderArray.Order.TransactionArray.Transaction.TransactionPrice',
        ]
    })
    if page == 1:
        pagination = response.reply.PaginationResult
        print('Found {} orders over {} pages'.format(
            pagination.TotalNumberOfEntries, pagination.TotalNumberOfPages))
    # with open('orders.json', 'w') as fp:
    #     json.dump(response.dict(), fp, indent=2)
    return response


def get_all_orders():
    for page in itertools.count(1):
        response = get_orders(page)
        reply = response.reply
        print('Page {}, {} items'.format(page, reply.ReturnedOrderCountActual))
        orders = response.dict()['OrderArray']['Order']
        for order in orders:
            yield order
        if reply.PageNumber == reply.PaginationResult.TotalNumberOfPages:
            break


if __name__ == '__main__':
    print('Search range: {:YYYY-MM-DD} to {:YYYY-MM-DD}'.format(start, end))
    orders = list(get_all_orders())
    print('Got {} orders'.format(len(orders)))
    with open('orders.json', 'w') as fp:
        json.dump(orders, fp, indent=2)
