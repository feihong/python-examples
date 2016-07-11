from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))

api = Trading(config_file=None, **credentials)
response = api.execute('GetUser', {})
pprint(response.dict())
# print(response.reply)
