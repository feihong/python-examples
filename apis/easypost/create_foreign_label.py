"""
Source: https://github.com/EasyPost/easypost-python/blob/master/README.md

"""
import webbrowser
import os
import easypost


easypost.api_key = os.environ['EASYPOST_API_KEY']


from_address = easypost.Address.create(
  verify=["delivery"],
  name = "EasyPost",
  street1 = "118 2nd Street",
  street2 = "4th Floor",
  city = "San Francisco",
  state = "CA",
  zip = "94105",
  country = "US",
  phone = "415-456-7890"
)

to_address = easypost.Address.create(
    # verify=['delivery'],
    name='Dr. Steve Brule',
    company='The Receiving Company',
    street1='35 Albert St',
    city='Waterloo',
    state='ON',
    zip='N2L 5E2',
    country='CA',
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
print('Rate:', lowest_rate.rate)
print('Service:', lowest_rate.service)
if lowest_rate.service == 'FirstClassPackageInternationalService':
    shipment.buy(rate=lowest_rate)
    print('Tracking:', shipment.tracking_code)
    url = shipment.postage_label.label_url
    print('Label:', url)
    webbrowser.open(url)