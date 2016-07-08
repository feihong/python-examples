"""
Example of using the Yelp API

"""

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# Copy and paste the contents of the following page into the multiline string below:
# https://www.yelp.com/developers/manage_api_keys

API_CREDENTIALS = """\
Consumer Key 	xxxx
Consumer Secret 	xxx
Token 	xxxx
Token Secret 	xxxx"""

credentials = {}
for line in API_CREDENTIALS.splitlines():
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
    print(bus.name)
    print('%s (%s)' % (bus.location.address[0], bus.location.cross_streets))
    print('Categories:', ', '.join(c.name for c in bus.categories))
    print('Rating:', bus.rating)
    print('Review:', bus.snippet_text)
    print('-' * 80)
    print()
