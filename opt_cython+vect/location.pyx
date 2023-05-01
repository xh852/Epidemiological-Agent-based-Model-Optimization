import random
import math

def generate_random_location(location, float max_distance):
    """
    Randomly generates a new (x, y) location that is within a max distance from the given location.

    Args:
    - current_location: A tuple representing the (x, y) coordinates of the current location.
    - max_distance: A float representing the maximum distance an agent can reach out to within one timestamp.

    Returns:
    - A tuple representing the (x, y) coordinates of the new location.
    """
    cdef float x
    cdef float y
    x, y = location[0], location[1]
    cdef float angle = random.uniform(0, 2 * math.pi)
    cdef float r = random.uniform(0, max_distance)
    cdef float new_x = x + r * math.cos(angle)
    cdef float new_y = y + r * math.sin(angle)
    return (new_x, new_y)

def snap_to_edge(location, float xmin, float ymin, float xmax, float ymax):
    """
    Snaps a location to the nearest edge of a square if it's outside the square.

    Args:
    - location: A tuple representing the (x, y) coordinates of the location to check.
    - xmin: A float representing the x-coordinate of the lower-left corner of the square.
    - ymin: A float representing the y-coordinate of the lower-left corner of the square.
    - xmax: A float representing the x-coordinate of the upper-right corner of the square.
    - ymax: A float representing the y-coordinate of the upper-right corner of the square.

    Returns:
    - A tuple representing the snapped location.
    """
    cdef float x
    cdef float y
    x, y = location[0], location[1]
    if x < xmin:
        x = xmin
    elif x > xmax:
        x = xmax
    if y < ymin:
        y = ymin
    elif y > ymax:
        y = ymax
    return (x, y)