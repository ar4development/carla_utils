import xml.etree.ElementTree as ET

def extract_way_node_geopositions(osm_file_name: str, road_name: str = None):
    """
    This method fetches lat and lon of nodes from osm file. You can either fetch road nodes if you set
    road_name value, or fetch all existing nodes (including buildings etc.)
    """
    file_name = osm_file_name
    tree = ET.parse(file_name)
    root = tree.getroot()
    path_to_lookup = ('./tag[@k="name"][@v="%s"]' % road_name) if road_name is not None else './*'
    ways = [w for w in root.findall('./way') if w.findall(path_to_lookup)]
    node_refs = []
    for way in ways:
        node_refs.extend([nr.attrib["ref"] for nr in way.findall("./nd")])
    nodes = []
    for node_ref in node_refs:
        xpath = "./node[@id='%s'][@visible='true']" % node_ref
        node = root.find(xpath)
        if node is not None:
            geo_position = (float(node.attrib['lat']), float(node.attrib['lon']))
            nodes.append(geo_position)
    return nodes


def extract_geo_origin_osm(osm_file_name: str):
    file_name = osm_file_name
    tree = ET.parse(file_name)
    root = tree.getroot()
    nodes = root.findall("node")
    lats = [float(node.attrib['lat']) for node in nodes]
    lons = [float(node.attrib['lon']) for node in nodes]
    result = min(lats), min(lons)
    print('Zero geo pos:', result)
    return result


def extract_offset_from_xodr(xodr_file_name):
    file_name = xodr_file_name
    tree = ET.parse(file_name)
    root = tree.getroot()
    header = root.find('./header')
    return float(header.attrib['west']), float(header.attrib['north'])