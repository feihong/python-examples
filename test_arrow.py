import arrow
from nose.tools import eq_


def test_six_months_ago():
    "Get the date of the first day of the month, six months ago"
    dt = arrow.get('2015-12-25')
    past = dt.replace(months=-6).replace(day=1)
    assert past.month == 6
    assert past.day == 1


def test_utf_offset():
    "Get the difference in hours between your local timezone and UTC."
    dt = arrow.now()
    hours_diff = dt.utcoffset().total_seconds() / 3600

    if dt.dst().total_seconds() == 0:
        eq_(hours_diff, -6.0)
    else:
        eq_(hours_diff, -5.0)


def test_get_datetime_for_day():
    import datetime
    dt = arrow.get(datetime.date.today())
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
