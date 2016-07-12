import datetime
from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

today = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
dt_start = today - datetime.timedelta(days=1)
dt_end = datetime.datetime.now()

response = api.execute('GetOrders', {
    'CreateTimeFrom': dt_start,
    'CreateTimeTo': dt_end,    
})
# response = api.execute('GetOrders', {'NumberOfDays': 1})
# pprint(response.dict())

orders = response.reply.OrderArray.Order

for order in orders:
    print(order.BuyerUserID)
    print(order.OrderStatus)
    print('Paid %s on %s' % (order.AmountPaid.value, order.PaidTime))
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

print('Received %d orders\n' % len(orders))
