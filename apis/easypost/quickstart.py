import os
import easypost

easypost.api_key = os.environ['EASYPOST_API_KEY']

to_address = easypost.Address.create(
  verify=['delivery'],
  name='Dr. Steve Brule',
  street1='179 N Harbor Dr',
  street2='',
  city='Redondo Beach',
  state='CA',
  zip='90277',
  country='US',
  phone='310-808-5243'
)
from_address = easypost.Address.create(
  verify=['delivery'],
  name='EasyPost',
  street1='118 2nd Street',
  street2='4th Floor',
  city='San Francisco',
  state='CA',
  zip='94105',
  country='US',
  phone='415-456-7890'
)

parcel = easypost.Parcel.create(
    predefined_package='Parcel',
    weight=0.34,
)

shipment = easypost.Shipment.create(
    to_address=to_address,
    from_address=from_address,
    parcel=parcel,
)

for rate in sorted(shipment.rates, key=lambda x: x.rate):
    print(rate.carrier, rate.service, rate.rate)
