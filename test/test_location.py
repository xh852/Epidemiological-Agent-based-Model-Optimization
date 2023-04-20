import math
from location import generate_random_location, snap_to_edge

def test_generate_random_location():
    # Test that the function returns a tuple of length 2
    location = (0, 0)
    distance = 1
    result = generate_random_location(location, distance)
    assert isinstance(result, tuple)
    assert len(result) == 2

    # Test that the function returns a location within the specified distance
    location = (0, 0)
    distance = 1
    for i in range(100):
        result = generate_random_location(location, distance)
        d = math.sqrt(result[0]**2 + result[1]**2)
        assert d <= distance

    # Test that the function returns a different location each time it's called
    location = (0, 0)
    distance = 1
    result1 = generate_random_location(location, distance)
    result2 = generate_random_location(location, distance)
    assert result1 != result2

def test_snap_to_edge():
    # Test a location inside the unit square
    location = (0.5, 0.5)
    snapped_location = snap_to_edge(location, 0, 0, 1, 1)
    assert snapped_location == (0.5, 0.5)

    # Test a location outside the unit square on the left
    location = (-0.5, 0.5)
    snapped_location = snap_to_edge(location, 0, 0, 1, 1)
    assert snapped_location == (0, 0.5)

    # Test a location outside the unit square on the right
    location = (1.5, 0.5)
    snapped_location = snap_to_edge(location, 0, 0, 1, 1)
    assert snapped_location == (1, 0.5)

    # Test a location outside the unit square on the bottom
    location = (0.5, -0.5)
    snapped_location = snap_to_edge(location, 0, 0, 1, 1)
    assert snapped_location == (0.5, 0)

    # Test a location outside the unit square on the top
    location = (0.5, 1.5)
    snapped_location = snap_to_edge(location, 0, 0, 1, 1)
    assert snapped_location == (0.5, 1)