import arrow


def test_six_months_ago():
    "Get the date of the first day of the month, six months ago"
    dt = arrow.get('2015-12-25')
    past = dt.replace(months=-6).replace(day=1)
    assert past.month == 6
    assert past.day == 1
