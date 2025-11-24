import pandas as pd
from pathlib import Path

def extract_data():
    df_covid=pd.read_csv('data/raw/worldwide-aggregate.csv', parse_dates=['Date'])

    return df_covid
