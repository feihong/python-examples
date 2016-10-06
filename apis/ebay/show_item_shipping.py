import os
import json
from ebaysdk.trading import Connection as Trading


credentials = dict(zip(('appid', 'devid', 'certid', 'token'), os.environ['EBAY_PARAMS'].split(';')))
api = Trading(config_file=None, **credentials)

response = api.execute('GetItem', {'ItemID': 182232608407})

with open('item.json', 'w') as fp:
    json.dump(response.dict(), fp, indent=2)

item = response.reply.Item
print(item.Title)

sd = item.ShippingDetails

# Possible values: USPSFirstClass, USPSPriorityFlatRateEnvelope,
# USPSPriorityMailPaddedFlatRateEnvelope, ShippingMethodStandard, ...
print('Domestic shipping service: {}'.format(
    sd.ShippingServiceOptions.ShippingService
))

print('International shipping services:')
for option in sd.InternationalShippingServiceOption:
    print('- {}'.format(option.ShippingService))

spd = item.ShippingPackageDetails

print('{} lb, {} oz'.format(spd.WeightMajor.value, spd.WeightMinor.value))

weight = int(spd.WeightMajor.value) *  16 + int(spd.WeightMinor.value)
print('Weight in oz: {}'.format(weight))
