"""
Source: https://github.com/EasyPost/easypost-python/blob/master/README.md

"""
import webbrowser
import os
import easypost


easypost.api_key = os.environ['EASYPOST_API_KEY']


from_address = easypost.Address.create(
    verify=['delivery'],
    name='Hugo Strongola',
    street1='126 Paddock Street',
    city='Crystal Lake',
    state='IL',
    zip='60014',
    country='US',
    phone='403-504-5496'
)

to_address = easypost.Address.create(
  verify=['delivery'],
  name='Dr. Steve Brule',
  street1='400 State Street',
  street2='',
  city='Chicago',
  state='IL',
  zip='60605',
  country='US',
  phone='310-808-5243'
)

parcel = easypost.Parcel.create(
    predefined_package='Parcel',
    weight=1,
)

shipment = easypost.Shipment.create(
    from_address=from_address,
    to_address=to_address,
    parcel=parcel,
)


lowest_rate = shipment.lowest_rate()
if lowest_rate.service == 'First':
    shipment.buy(rate=lowest_rate)
    print('Tracking:', shipment.tracking_code)
    url = shipment.postage_label.label_url
    print('Label:', url)
    webbrowser.open(url)
