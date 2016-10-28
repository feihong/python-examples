import os
import easypost


easypost.api_key = os.environ['EASYPOST_API_KEY']

weights = list(range(1, 17)) + [15.99999]
# weights = [1]


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


for weight in weights:
    parcel = easypost.Parcel.create(
        predefined_package='Parcel',
        weight=weight,
    )
    shipment = easypost.Shipment.create(
        from_address=from_address,
        to_address=to_address,
        parcel=parcel,
    )
    rate = [rate for rate in shipment.rates if rate.service == 'First'][0]
    print('{} oz: {}'.format(weight, rate.rate))
