"""
Source: https://github.com/EasyPost/easypost-python/blob/master/README.md

Customs guide: https://www.easypost.com/customs-guide.html

EasyPost's foreign-bound labels are 1755 × 1155.

You can visit http://hts.usitc.gov/ to search for valid values for the
hs_tariff_number field. You only need to pass the first six digits, without the
periods.

If the value of the goods is less than $2,500, then the value of the eel_pfc
field should be "NOEEI 30.37(a)"

"""
import webbrowser
import os
import easypost


easypost.api_key = os.environ['EASYPOST_API_KEY']

weight = 1


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
    weight=weight,
)

customs_item = easypost.CustomsItem.create(
    description = 'EasyPost Mug',
    origin_country='CN',
    quantity=1,
    value=25.45,
    weight=weight,
    hs_tariff_number=820770,
)

customs_info = easypost.CustomsInfo.create(
    customs_certify=True,       # should always be True
    customs_signer='Hector Hammerfist',
    contents_type='gift',
    contents_explanation=None,  # only needed if contents_type is 'other'
    eel_pfc='NOEEI 30.37(a)',
    non_delivery_option='return',
    restriction_type='none',
    restriction_comments=None,  # only needed if restriction_type is 'other'
    customs_items=[customs_item]
)

shipment = easypost.Shipment.create(
    from_address=from_address,
    to_address=to_address,
    parcel=parcel,
    customs_info=customs_info,
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
