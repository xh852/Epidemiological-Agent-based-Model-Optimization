import unittest
from location import generate_random_location, snap_to_edge

class TestLocation(unittest.TestCase):

    def test_generate_random_location(self):
        current_location = (0.5, 0.5)
        max_distance = 0.1
        new_location = generate_random_location(current_location, max_distance)
        distance = ((current_location[0] - new_location[0])**2 + (current_location[1] - new_location[1])**2)**0.5
        self.assertLessEqual(distance, max_distance)

    def test_snap_to_edge(self):
        location = (-0.1, 0.5)
        min_x, min_y, max_x, max_y = 0, 0, 1, 1
        snapped_location = snap_to_edge(location, min_x, min_y, max_x, max_y)
        self.assertTrue(min_x <= snapped_location[0] <= max_x)
        self.assertTrue(min_y <= snapped_location[1] <= max_y)

if __name__ == '__main__':
    unittest.main()
