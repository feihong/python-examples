"""
Fetch historical orders based on a datetime range, but exclude most fields in
the response.

"""
import os
import datetime
import json
import arrow
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

start = arrow.utcnow().replace(days=-120).replace(
    hour=0, minute=0, second=0, microsecond=0)
end = start.replace(days=+50)

response = api.execute('GetOrders', {
    'CreateTimeFrom': start,
    'CreateTimeTo': end,
    'OrderStatus': 'Completed',
    'OutputSelector': [
        'PageNumber',
        'PaginationResult',
        'OrderArray.Order.TransactionArray.Transaction.Item.ItemID',
    ]
})
with open('orders.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

orders = response.reply.OrderArray.Order

print('Search range: {:YYYY-MM-DD} to {:YYYY-MM-DD}'.format(start, end))

pagination = response.reply.PaginationResult
print('Received {} entries in {} pages'.format(
    pagination.TotalNumberOfEntries, pagination.TotalNumberOfPages))
