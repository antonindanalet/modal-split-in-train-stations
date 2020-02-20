import pandas as pd
from pathlib import Path


def get_etappen(year, selected_columns=None):
    folder_path_2015 = Path('../data/input/')
    if year == 2015:
        with open(folder_path_2015 / 'etappen.csv', 'r') as etappen_file:
            df_etappen = pd.read_csv(etappen_file,
                                     dtype={'HHNR': int,
                                            'W_AGGLO_GROESSE2012': int},
                                     usecols=selected_columns)
    else:
        raise Exception('Year not (yet) defined.')
    return df_etappen
