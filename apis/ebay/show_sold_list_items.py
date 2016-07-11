from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetMyeBaySelling', {
    'SoldList': {
        'Include': True
    }
})
# pprint(response.dict())

orders = response.reply.SoldList.OrderTransactionArray.OrderTransaction

for order in orders:
    buyer = order.Transaction.Buyer
    print(buyer.UserID)
    print(order.Transaction.Item.Title)
    print(buyer.BuyerInfo.ShippingAddress)
    print('=' * 80)
