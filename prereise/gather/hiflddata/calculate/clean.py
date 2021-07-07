import pandas as pd


def clean_substations(df, zone_dic):
    return df.query("STATE in @zone_dic and LINES != 0")


def clean_lines(raw_data):
    """Create dict to store all the raw transmission line csv data

    :param str t_csv: path of the HIFLD transmission csv file
    :return: (*dict*) -- a dict mapping the transmission ID to its raw parameters.
    """

    raw_data["ID"] = raw_data["ID"].astype("str")
    raw_lines = raw_data.set_index("ID").to_dict()
    return raw_lines
