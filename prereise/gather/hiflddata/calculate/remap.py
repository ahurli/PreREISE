import pandas as pd

def get_zone_mapping(zone):
    """Generate a dictionary of zone using the zone.csv

    :param pandas.DataFrame zone: the zone.csv data
    :return: (*dict*) -- a dict mapping the STATE to its ID.
    """

    # Create dictionary to store the mapping of states and codes
    zone_dic = {}
    zone_dic1 = {}
    for i in range(len(zone)):
        tu = (zone["zone_name"][i], zone["interconnect"][i])
        zone_dic[zone["zone_name"][i]] = zone["zone_id"][i]
        zone_dic1[tu] = zone["zone_id"][i]
    return zone_dic, zone_dic1

