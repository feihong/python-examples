import re
import os
import json
from ebaysdk.trading import Connection as Trading


ITEM_IDS = """\
131429151455
131428961568
131826828485
141576946029
131436535970
131405144230
141544268932
131405144214
141543584884
131405682552
141544268933
131405682551
131813094764""".splitlines()


LOCATIONS = ['Americas', 'Europe', 'Asia', 'GB', 'CN', 'MX', 'DE', 'JP', 'BR', 'FR', 'AU', 'RU']


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))

for item_id in ITEM_IDS:
    trading = Trading(config_file=None, **credentials)
    response = trading.execute('GetItem', {
        'ItemID': item_id,
    })
    item = response.reply.Item

    shipping = {}
    options = item.ShippingDetails.ShippingServiceOptions
    shipping['us'] = options.ShippingServiceCost.value
    shipping['us_add'] = options.ShippingServiceAdditionalCost.value

    options = item.ShippingDetails.InternationalShippingServiceOption

    option = [o for o in options if o.ShipToLocation == 'CA'][0]
    shipping['ca'] = option.ShippingServiceCost.value
    shipping['ca_add'] = option.ShippingServiceAdditionalCost.value

    option = [o for o in options if o.ShipToLocation == LOCATIONS][0]
    shipping['intl'] = option.ShippingServiceCost.value
    shipping['intl_add'] = option.ShippingServiceAdditionalCost.value

    for k in shipping.keys():
        v = float(shipping[k])
        if v % 1:
            v = '%0.2f' % v
        else:
            v = '%0.0f' % v
        shipping[k] = v

    shipping_str = '{us}/{us_add}, {ca}/{ca_add}, {intl}/{intl_add}'.format(**shipping)

    print('{title}\t{url}\t{price}\t{shipping}'.format(
        title=item.Title,
        url='http://www.ebay.com/itm/' + item_id,
        price=item.StartPrice.value,
        shipping=shipping_str,
    ))
