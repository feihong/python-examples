"""
Example of using the FourSquare API

Dependency:

pip install foursquare

"""
import foursquare

CLIENT_ID = 'xxx'
CLIENT_SECRET = 'xxx'

client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

params = dict(
    near='4950 N Western Ave, Chicago, IL',
    radius=1600,
    section='food',
    venuePhotos=1,
    openNow=1,
    sortByDistance=1,
)
resp = client.venues.explore(params=params)

for group in resp['groups']:
    for item in group['items']:
        venue = item['venue']
        print(venue['name'])
        print(venue['location']['formattedAddress'][0])
        print('Rating:', venue['rating'])
        categories = (c['shortName'] for c in venue['categories'])
        print('Categories:', ', '.join(categories))
        print('-' * 80)
        print()
