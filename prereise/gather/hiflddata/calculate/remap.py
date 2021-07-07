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

def get_sub_mapping(clean_data):
    """Generate the subs

    :param str E_csv: path of the HIFLD substation csv file
    :return: (*dict*) --  sub_by_coord_dict, a dict mapping from (x, y) to substation detail.
    :return: (*dict*) --  sub_name_dict, a dict mapping from substation name to its coordinate (x, y).
    """

    sub_by_coord_dict = {}
    sub_name_dict = {"sub": []}
    for index, row in clean_data.iterrows():
        location = (row["LATITUDE"], row["LONGITUDE"])
        if location in sub_by_coord_dict:
            raise Exception(
                f"WARNING: substations coordinates conflict check: {location}"
            )
        sub_by_coord_dict[location] = (
            row["ID"],
            row["NAME"],
            row["STATE"],
            row["COUNTY"],
        )
        if row["NAME"] not in sub_name_dict:
            sub_name_dict[row["NAME"]] = []
        sub_name_dict[row["NAME"]].append((row["LATITUDE"], row["LONGITUDE"]))
    return sub_by_coord_dict, sub_name_dict    
