import carla


def convert_osm_map_to_xodr(osm_path, xodr_path):

    # Read the .osm data
    f = open(osm_path, 'r', encoding="utf-8")  # Windows will need to encode the file in UTF-8. Read the note below.
    osm_data = f.read()
    f.close()

    # Define the desired settings. In this case, default values.
    settings = carla.Osm2OdrSettings()
    settings.elevation_layer_height = 3.5
    # Convert to .xodr
    xodr_data = carla.Osm2Odr.convert(osm_data, settings)

    # save opendrive file
    f = open(xodr_path, 'w', encoding="utf-8")
    f.write(xodr_data)
    f.close()


def draw_points(file_path):
    col_normal = carla.Color(0, 255, 0)
    import osm_utils as esn
    geo_coords = esn.extract_way_node_geopositions(file_path)
    original_zero_lat, original_zero_lon = esn.extract_geo_origin_osm(
        file_path)
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    # Draw axes where red is Y and blue is X
    world.debug.draw_line(carla.Location(0, -3000, 0),
                               carla.Location(0, 3000, 0), 2, carla.Color(255, 0, 0), -1.0, True)
    world.debug.draw_line(carla.Location(-3000, 0, 0),
                               carla.Location(3000, 0, 0), 2, carla.Color(0, 0, 255), -1.0, True)
    import geo
    for coord in geo_coords:
        lat, lon = coord
        x, y = geo.calculate_new_center_delta(original_zero_lat, original_zero_lon, lat, lon)
        if -10 < x < 10:
            print('drawing: ', x, y)
        line_begin = carla.Location(x, -y, 0)
        line_end = carla.Location(x, -y, 3)
        world.debug.draw_line(line_begin, line_end, 10, col_normal, -1.0, True)


if __name__ == '__main__':
    pass
    # convert_osm_map_to_xodr('/home/maps/scenario_ready.osm', '/home/maps/latest_road.xodr')
    # Load map to Carla here
    # draw_points('/home/maps/scenario_ready.osm')
