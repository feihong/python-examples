from pprint import pprint
import os
from ebaysdk.trading import Connection as Trading


params = os.environ['EBAY_PARAMS'].split(';')
credentials = dict(appid=params[0], devid=params[1], certid=params[2], token=os.environ['EBAY_USER_TOKEN'], config_file=None)


api = Trading(**credentials)
response = api.execute('GetUser', {})
pprint(response.dict())
# print(response.reply)
