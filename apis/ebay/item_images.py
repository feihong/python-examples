"""
For a given item, prints out the full size image URLs from its gallery.

"""
import re
import os
from pprint import pprint
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {'ItemID': '172064937927'})
# pprint(response.dict())

item = response.reply.Item
print(item.Title + '\n')
urls = item.PictureDetails.PictureURL

url_pattern = re.compile(r'\/z\/(.*)\/\$')
for url in urls:
    # print(url)
    image_id = url_pattern.search(url).group(1)
    fullsize_url = 'http://i.ebayimg.com/images/g/%s/s-l1600.jpg' % image_id
    print(fullsize_url)
    print()
