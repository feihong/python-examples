from geopy.distance import vincenty


def test_vincenty():
    "vincenty() returns a good approximate distance between two points"
    # Note that these points have the format (latitude, longitude).
    point1 = (41.957773, -87.681529)
    point2 = (41.966305, -87.688460)
    assert vincenty(point1, point2).miles == 0.6886357832105573
