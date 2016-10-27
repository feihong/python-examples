"""
Fetch historical orders based on a datetime range.

"""
import arrow
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

start = arrow.utcnow().replace(days=-90)
end = start.replace(days=+1)

response = api.execute('GetOrders', {
    'CreateTimeFrom': start,
    'CreateTimeTo': end,
    'OrderStatus': 'Completed',
})

orders = response.reply.OrderArray.Order
orders.sort(key=lambda x: x.CreatedTime)

for order in orders:
    print(order.OrderID)
    print(order.BuyerUserID)
    print('Created %s' % order.CreatedTime)
    print('Paid %s on %s' % (order.AmountPaid.value, order.PaidTime))
    print('Shipped %s' % getattr(order, 'ShippedTime', 'N/A'))

    transactions = order.TransactionArray.Transaction
    for transaction in transactions:
        print('-', transaction.Item.Title)
    print('='*70)

print('Received {} orders for range {:YYYY-MM-DD} to {:YYYY-MM-DD}'.format(
    len(orders), start, end))
