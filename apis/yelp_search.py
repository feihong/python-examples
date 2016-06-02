"""
Example of using the Yelp API

Dependency:

pip install yelp

"""

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# The config_secret.txt file should contain the pasted contents of this page:
# https://www.yelp.com/developers/manage_api_keys

credentials = {}
with open('config_secret.txt') as fp:
    for line in fp.readlines():
        key, value = line.split('\t')
        credentials[key.strip().lower().replace(' ', '_')] = value.strip()


auth = Oauth1Authenticator(
    consumer_key=credentials['consumer_key'],
    consumer_secret=credentials['consumer_secret'],
    token=credentials['token'],
    token_secret=credentials['token_secret']
)

client = Client(auth)

resp = client.search(
    '2501 W Lawrence Ave, Chicago, IL',
    category_filter='restaurants',
    radius_filter=1600)

businesses = (b for b in resp.businesses if not b.is_closed)

for bus in businesses:
    print bus.name
    print '%s (%s)' % (bus.location.address[0], bus.location.cross_streets)
    print 'Categories:', ', '.join(c.name for c in bus.categories)
    print 'Rating:', bus.rating
    print 'Review:', bus.snippet_text
    print '-' * 80
    print
