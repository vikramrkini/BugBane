import math

EARTH_RADIUS = 6371  # km

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two geographic coordinates using the haversine formula.

    Args:
        lat1 (float): Latitude of the first coordinate in degrees.
        lon1 (float): Longitude of the first coordinate in degrees.
        lat2 (float): Latitude of the second coordinate in degrees.
        lon2 (float): Longitude of the second coordinate in degrees.

    Returns:
        float: The distance between the two coordinates in kilometers.
    """
    lat1_r = math.radians(lat1)
    lon1_r = math.radians(lon1)
    lat2_r = math.radians(lat2)
    lon2_r = math.radians(lon2)

    d_lat = lat2_r - lat1_r
    d_lon = lon2_r - lon1_r

    a = math.sin(d_lat / 2)**2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance
