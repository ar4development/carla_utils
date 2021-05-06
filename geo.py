from math import cos, pi


def calculate_new_center_delta(old_lat, old_lon, new_lat, new_lon):
    """
    we will need that later when we'll be able to bind to a concrete
    geo position on the map..
    """
    lat_factor = 111111.111111
    lon_factor = 111300.0 * cos(pi * old_lat / 180.0)
    x = (new_lon - old_lon) * lon_factor
    y = (new_lat - old_lat) * lat_factor
    print(old_lat, old_lon, new_lat, new_lon, x ,y)
    return x, y

