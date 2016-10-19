import datetime
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetOrders', {'NumberOfDays': 2})
# pprint(response.dict())

today = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
yesterday = today - datetime.timedelta(days=1)
paid_count = 0

orders = response.reply.OrderArray.Order

for order in orders:
    if order.PaidTime < yesterday:
        continue
    paid_count += 1
    print(order.OrderID)
    print(order.BuyerUserID)
    print(order.OrderStatus)
    print('Created %s' % order.CreatedTime)
    print('Paid %s on %s' % (order.AmountPaid.value, order.PaidTime))
    print('Shipped %s' % order.ShippedTime)
    transactions = order.TransactionArray.Transaction
    item_titles = '; '.join(t.Item.Title for t in transactions)
    print(item_titles)
    item_ids = ', '.join(t.Item.ItemID for t in transactions)
    print(item_ids)
    sa = order.ShippingAddress
    address = '%s\n%s\n%s\n%s, %s %s' % (sa.Name, sa.Street1, sa.Street2, sa.CityName, sa.CountryName, sa.PostalCode)
    print(address)
    print('=' * 80)
    # import ipdb; ipdb.set_trace()

print('Received %d orders' % len(orders))
print('%d orders were paid for since yesterday' % paid_count)
