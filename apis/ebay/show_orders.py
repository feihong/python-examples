from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetOrders', {'NumberOfDays': 1})
# pprint(response.dict())

orders = response.reply.OrderArray.Order
print('Received %d orders\n' % len(orders))
for order in orders:
    print(order.BuyerUserID)
    print(order.OrderStatus)
    transactions = order.TransactionArray.Transaction
    item_titles = ' AND '.join(t.Item.Title for t in transactions)
    print(item_titles)
    sa = order.ShippingAddress
    address = '%s\n%s\n%s\n%s, %s %s' % (sa.Name, sa.Street1, sa.Street2, sa.CityName, sa.CountryName, sa.PostalCode)
    print(address)
    print('=' * 80)
    # import ipdb; ipdb.set_trace()
