import json
from pprint import pprint


TRACKING_NUMBERS = [
    '9400109699938067974989', '9400109699938067974996',
    '9400109699938067974972', '9400109699937209328758',
    '9400109699938067974927', '9400109699938067974965',
    '9400109699937209328680', '9400109699938067974958',
    '9400109699939560594780', '9400109699937209328741',
    '9400109699937209328727', 'LZ539632982US'
]


def main():
    orders = json.load(open('orders.json'))
    map = get_tracking_number_map(orders)

    for tn in TRACKING_NUMBERS:
        order = map[tn]
        if order is not None:
            print('{}: {}'.format(tn, order['BuyerUserID']))
            sa = order['ShippingAddress']
            print('{Name}\n{Street1}\n{CityName}, {StateOrProvince} {PostalCode}'.format(**sa))
            print('='*75)


def get_tracking_number_map(orders):
    result = {}
    for order in orders:
        tn = get_tracking_number(order)
        if tn is not None:
            result[tn] = order
    return result


def get_tracking_number(order):
    tracking_nums = []
    transactions = order['TransactionArray']['Transaction']
    for transaction in transactions:
        try:
            tn = (transaction['ShippingDetails']['ShipmentTrackingDetails']
                ['ShipmentTrackingNumber'])
            tracking_nums.append(tn)
        except KeyError:
            pass

    if len(tracking_nums) == 0:
        return None

    # Make sure that all tracking nums are the same.
    assert all(n == tracking_nums[0] for n in tracking_nums)
    return tracking_nums[0]


if __name__ == '__main__':
    main()
