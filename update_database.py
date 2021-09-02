import os
import requests
from covidgraphs.constants import DATA_DIR, COVID_DATA_FILE, COVID_DATA_URL
import logging
import pandas as pd
from pandas import DataFrame

def get_newest_data() -> DataFrame:
    """Downloads the newest covid data"""
    logging.info("Getting newest covid data")
    page = requests.get(COVID_DATA_URL)

    with open(COVID_DATA_FILE,'w') as f:
        f.write(page.text)

    # parse the csv data and save
    df = parse_csv_data()
    return df

def parse_csv_data() -> DataFrame:
    """Turn the csv file into a dataframe"""
    logging.info("parsing csv data")
    df = pd.read_csv(COVID_DATA_FILE)

    df.date.map(pd.to_datetime)
    df.set_index('date',inplace=True)

    df.to_pickle(os.path.join(DATA_DIR,'covid_data.pickle'))

    return df

if __name__ == '__main__':
    get_newest_data()
