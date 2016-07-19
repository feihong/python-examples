from pprint import pprint
import os
from ebaysdk.shopping import Connection as Shopping


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Shopping(config_file=None, **credentials)

response = api.execute('GetSingleItem', {'ItemID': 171992581889})
# pprint(response.dict())

item = response.reply.Item
