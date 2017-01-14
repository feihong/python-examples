import attr
from nose.tools import eq_

@attr.s
class TrackingNumber:
    type = attr.ib(default='')
    value = attr.ib(default='')


@attr.s(repr=False)
class Animal:
    name = attr.ib(default='')
    limbs = attr.ib(default=0)

    def __repr__(self):
        return 'Animal({}, {})'.format(self.name, self.limbs)


def test_automatic_repr_method():
    tn = TrackingNumber(type='domestic top', value='LZ332003764US')

    eq_('{}'.format(tn), "TrackingNumber(type='domestic top', value='LZ332003764US')")
    eq_(repr(tn), "TrackingNumber(type='domestic top', value='LZ332003764US')")


def test_use_own_repr_method():
    animal = Animal(name='Bobcat', limbs=4)

    eq_(repr(animal), 'Animal(Bobcat, 4)')
