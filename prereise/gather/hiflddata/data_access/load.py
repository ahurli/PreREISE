import pandas as pd

def load_csv(csv_filename):
    data = pd.read_csv(csv_filename)
    return data
