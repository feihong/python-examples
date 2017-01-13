"""
Fetch orders given a datetime range. Retrieve all pages that match the
request criteria.

"""
import os
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
        'ModTimeFrom': start,
        'ModTimeTo': end,
        'OrderStatus': 'Completed',
    })
    pagination = response.reply.PaginationResult
    print('Page {} of {}: {} orders'.format(
        page,
        pagination.TotalNumberOfPages,
        response.reply.ReturnedOrderCountActual))
    return response


def get_tracking_numbers(order):
    result = []
    transactions = order['TransactionArray']['Transaction']
    for transaction in transactions:
        try:
            tn = (transaction['ShippingDetails']['ShipmentTrackingDetails']
                ['ShipmentTrackingNumber'])
            result.append(tn)
        except KeyError:
            pass

    return result


def print_orders():
    orders = json.load(open('orders.json'))
    for order in orders:
        print(order['ShippingAddress']['Name'])
        mod_time = arrow.get(order['CheckoutStatus']['LastModifiedTime']).to('US/Central')
        print(mod_time.format('YYYY-MM-DD hh:mm A'))
        print(', '.join(get_tracking_numbers(order)))
        print('='*75)


if __name__ == '__main__':
    now = arrow.utcnow()
    start = now.replace(days=-1)
    end = now

    print('Search range: {} to {}'.format(start, end))
    orders = list(get_orders(start, end))
    print('Got {} orders'.format(len(orders)))
    with open('orders.json', 'w') as fp:
        json.dump(orders, fp, indent=2)

    print_orders()
