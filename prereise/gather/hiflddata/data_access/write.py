import csv
import pandas as pd

West = ["WA", "OR", "CA", "NV", "AK", "ID", "UT", "AZ", "WY", "CO", "NM"]
Uncertain = ["MT", "SD", "TX"]

def write_grid(clean_data, region, zone_dic, zone_dic1, kv_dict, lines):
    re_code, sub_code = write_sub(clean_data, zone_dic, zone_dic1, region)
    write_bus(clean_data, sub_code, re_code, kv_dict)
    write_bus2sub(clean_data, re_code)
    lines["interconnect"] = lines.apply(
        lambda row: re_code.get(row["from_bus_id"]), axis=1
    )
    write_branch(lines)
    

def write_sub(clean_data, zone_dic, zone_dic1, region):
    """Write the data to sub.csv as output

    :param pandas.DataFrame clean_data: substation dataframe as returned by :func:`Clean`
    :param dict zone_dic: zone dict as returned by :func:`get_Zone`
    """
    tx_west = ["EL PASO", "HUDSPETH"]
    tx_east = [
        "BOWIE",
        "MORRIS",
        "CASS",
        "CAMP",
        "UPSHUR",
        "GREGG",
        "MARION",
        "HARRISON",
        "PANOLA",
        "SHELBY",
        "SAN AUGUSTINE",
        "SABINE",
        "JASPER",
        "NEWTON",
        "ORANGE",
        "JEFFERSON",
        "LIBERTY",
        "HARDIN",
        "TYLER",
        "POLK",
        "TRINITY",
        "WALKER",
        "SAN JACINTO",
        "DALLAM",
        "SHERMAN",
        "HANSFORD",
        "OCHLTREE" "LIPSCOMB",
        "HARTLEY",
        "MOORE",
        "HUTCHINSON",
        "HEMPHILL",
        "RANDALL",
        "DONLEY",
        "PARMER",
        "BAILEY",
        "LAMB",
        "HALE",
        "COCHRAN",
        "HOCKLEY",
        "LUBBOCK",
        "YOAKUM",
        "TERRY",
        "LYNN",
        "GAINES",
    ]

    sd_west = ["LAWRENCE", "BUTTE", "FALL RIVER"]
    # nm_east = ['CURRY', 'LEA', 'QUAY', 'ROOSEVELT', 'UNION']
    mt_east = [
        "CARTER",
        "CUSTER",
        "ROSEBUD",
        "PRAIRIE",
        "POWDER RIVER",
        "DANIELS",
        "MCCONE",
        "DAWSON",
        "RICHLAND",
        "FALLON",
        "GARFIELD",
        "ROOSEVELT",
        "PHILLIPS",
        "SHERIDAN",
        "VALLEY",
        "WIBAUX",
    ]
    sub = open("output/sub.csv", "w", newline="")
    csv_writer = csv.writer(sub)
    csv_writer.writerow(
        [
            "sub_id",
            "name",
            "zip",
            "lat",
            "lon",
            "interconnect",
            "zone_id",
            "type",
            "state",
        ]
    )
    sub_code = {}
    re_code = {}
    for index, row in clean_data.iterrows():
        if row["STATE"] in West:
            re = "Western"
        elif row["STATE"] in Uncertain:
            if row["STATE"] == "TX":
                if row["COUNTY"] in tx_west:
                    re = "Western"
                elif row["COUNTY"] in tx_east:
                    re = "Eastern"
                else:
                    re = "Texas"

            elif row["STATE"] == "SD":
                if row["COUNTY"] in sd_west:
                    re = "Western"
                else:
                    re = "Eastern"
            elif row["STATE"] == "MT":
                if row["COUNTY"] in mt_east:
                    re = "Eastern"
                else:
                    # code = zone_dic1[(row['STATE'],re)]
                    re = "Western"
        else:
            re = "Eastern"

        code = zone_dic1[(row["STATE"], re)]
        sub_code[row["ID"]] = code
        re_code[row["ID"]] = re
        csv_writer.writerow(
            [
                row["ID"],
                row["NAME"],
                row["ZIP"],
                row["LATITUDE"],
                row["LONGITUDE"],
                re,
                code,
                row["TYPE"],
                row["STATE"],
            ]
        )

    sub.close()

    return re_code, sub_code
    
def write_bus(clean_data, sub_code, re_code, kv_dict):
    """Write the data to bus.csv as output

    :param pandas.DataFrame clean_data: substation dataframe as returned by :func:`Clean`
    :param dict zone_dic: zone dict as returned by :func:`get_Zone`
    :param dict kv_dict: substation KV dict
    """

    with open("output/bus.csv", "w", newline="") as bus:
        csv_writer = csv.writer(bus)
        csv_writer.writerow(
            [
                "bus_id",
                "type",
                "Pd",
                "Qd",
                "Gs",
                "Bs",
                "zone_id",
                "Vm",
                "Va",
                "baseKV",
                "loss_zone",
                "Vmax",
                "Vmin",
                "lam_P",
                "lam_Q",
                "mu_Vmax",
                "mu_Vmin",
                "interconnect",
                "state",
            ]
        )
        missing_sub = []
        for index, row in clean_data.iterrows():
            sub = (row["LATITUDE"], row["LONGITUDE"])
            if sub in kv_dict:
                csv_writer.writerow(
                    [
                        row["ID"],
                        1,
                        round(row["Pd"], 3),
                        0.0,
                        0.0,
                        0.0,
                        sub_code[row["ID"]],
                        0.0,
                        0.0,
                        kv_dict[sub],
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        re_code[row["ID"]],
                        row["STATE"],
                    ]
                )
            else:
                missing_sub.append(sub)

    print(
        "INFO: ",
        len(missing_sub),
        " substations excluded from the network. Some examples:",
    )
    print(missing_sub[:20])

def write_bus2sub(clean_data, re_code):
    """Write the data to bus2sub.csv as output

    :param pandas.DataFrame clean_data: substation dataframe as returned by :func:`Clean`
    """

    with open("output/bus2sub.csv", "w", newline="") as bus2sub:
        csv_writer = csv.writer(bus2sub)
        csv_writer.writerow(["bus_id", "sub_id", "interconnect"])
        for index, row in clean_data.iterrows():
            csv_writer.writerow([row["ID"], row["ID"], re_code[row["ID"]]])


def write_branch(lines):
    """Write the data to branch.csv as output

    :param list lines:  a list of lines as returned by :func:`Neighbors`
    """
    branch = open("output/branch.csv", "w", newline="")
    phase = open("output/Phase Shifter.csv", "w", newline="")
    dc = open("output/dcline.csv", "w", newline="")

    csv_writer = csv.writer(branch)
    csv_writer1 = csv.writer(phase)
    csv_writer2 = csv.writer(dc)
    csv_writer.writerow(
        [
            "branch_id",
            "from_bus_id",
            "to_bus_id",
            "r",
            "x",
            "b",
            "rateA",
            "rateB",
            "rateC",
            "ratio",
            "angle",
            "status",
            "angmin",
            "angmax",
            "Pf",
            "Qf",
            "Qt",
            "mu_Sf",
            "mu_St",
            "mu_angmin",
            "mu_angmax",
            "branch_device_type",
            "interconnect",
        ]
    )
    csv_writer1.writerow(
        [
            "branch_id",
            "from_bus_id",
            "to_bus_id",
            "r",
            "x",
            "b",
            "rateA",
            "rateB",
            "rateC",
            "ratio",
            "angle",
            "status",
            "angmin",
            "angmax",
            "Pf",
            "Qf",
            "Qt",
            "mu_Sf",
            "mu_St",
            "mu_angmin",
            "mu_angmax",
            "branch_device_type",
            "interconnect",
        ]
    )
    csv_writer2.writerow(
        [
            "dcline_id",
            "from_bus_id",
            "to_bus_id",
            "status",
            "Pf",
            "Pt",
            "Qf",
            "Qt",
            "Vf",
            "Vt",
            "Pmin",
            "Pmax",
            "QminF",
            "QmaxF",
            "QminT",
            "QmaxT",
            "loss0",
            "loss1",
            "muPmin",
            "muPmax",
            "muQminF",
            "muQmaxF",
            "from_interconnect",
            "to_interconnect",
        ]
    )
    bus_pd = pd.read_csv("output/bus.csv")
    bus_dict = {}
    for bus in bus_pd.iloc():
        bus_dict[bus["bus_id"]] = bus["interconnect"]
    for _, row in lines.iterrows():
        if row["line_type"] == "DC":
            from_connect = bus_dict[row["from_bus_id"]]
            to_connect = bus_dict[row["to_bus_id"]]
            csv_writer2.writerow(
                [
                    row["branch_id"],
                    row["from_bus_id"],
                    row["to_bus_id"],
                    1,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    -200,
                    200,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    from_connect,
                    to_connect,
                ]
            )
        else:
            csv_writer.writerow(
                [
                    row["branch_id"],
                    row["from_bus_id"],
                    row["to_bus_id"],
                    0.0,
                    row["reactance"],
                    0.0,
                    row["rateA"],
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    row["line_type"],
                    row["interconnect"],
                ]
            )
    branch.close()
    phase.close()
    dc.close()


"""
        elif row['line_type'] == 'Phase Shifter':
            csv_writer1.writerow(
                [
                    row["branch_id"],
                    row["from_bus_id"],
                    row["to_bus_id"],
                    0.0,
                    row["reactance"],
                    0.0,
                    row["rateA"],
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    row["line_type"],
                    row["interconnect"]
                ])
"""
    
