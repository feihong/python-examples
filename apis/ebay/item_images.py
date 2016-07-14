"""
For a given item, prints out the full size image URLs from its gallery.

"""
import re
import os
import subprocess
from pprint import pprint
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {'ItemID': '142026412435'})
# pprint(response.dict())

item = response.reply.Item
print(item.Title + '\n')
urls = item.PictureDetails.PictureURL

url_pattern = re.compile(r'\/z\/(.*)\/\$')
for i, url in enumerate(urls, 1):
    print('%d. %s' % (i, url))
    # subprocess.call(['wget', '-O', '%d.jpg' % i, url])
    print()
