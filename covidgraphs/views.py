import json
from django.http import JsonResponse
from functools import lru_cache
from django.shortcuts import render
import pandas as pd
import requests
import os
import time
from dateutil import parser
from pandas import DataFrame

from .constants import DATA_DIR,COVID_DATA_FILE,COVID_DATA_URL,LAST_UPDATE_URL,LAST_CHECK_FILE
from covidgraphs.templatetags.filter import parse_var

def newer_data_available()-> bool:
    """Returns true is newer data is available or no file is found"""
    # guard against no file
    if not os.path.isfile(COVID_DATA_FILE):
        return True

    # if last check was within the past hour then don't do anything.
    if os.path.isfile(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE) as f:
            last_check_time = f.readline()
            if time.time()-float(last_check_time) < 60*60:
                return False

    # check when the covid data file was last modified
    t = os.path.getmtime(COVID_DATA_FILE)
    page = requests.get(LAST_UPDATE_URL)
    return parser.parse(page.text).timestamp() < t

def get_newest_data() -> DataFrame:
    """Downloads the newest covid data"""
    page = requests.get(COVID_DATA_URL)

    with open(COVID_DATA_FILE,'w') as f:
        f.write(page.text)
    # put local file saying when the last check was to preventing pining the github server again and again
    with open(LAST_CHECK_FILE,'w') as f:
        f.writelines(f"{time.time()}")

    # parse the csv data and save
    df = parse_csv_data()
    return df

def parse_csv_data() -> DataFrame:
    """"""
    df = pd.read_csv(COVID_DATA_FILE)

    df.date.map(pd.to_datetime)
    df.set_index('date',inplace=True)

    df.to_pickle(os.path.join(DATA_DIR,'covid_data.pickle'))

    return df

@lru_cache(maxsize=1)
def load_dataframe() -> DataFrame:
    try:
        df = pd.read_pickle(os.path.join(DATA_DIR,'covid_data.pickle'))
    except FileNotFoundError:
        df = get_newest_data()
    finally:
        return df


# Create your views here.
def front(request):

    df = load_dataframe()
    countries = list(df['location'].unique())
    variables = [var for var in df.columns if var not in {"continent","iso_code","location"}]

    return render(request,"covidgraphs/front_page.html",{"countries":countries,"variables":variables})

def graph_data(request) -> JsonResponse:
    """Returns data based on the request"""

    if newer_data_available():
        df = get_newest_data()
    else:
        df = load_dataframe()

    query = request.POST
    var1 = request.POST['var1']
    var2 = request.POST['var2']

    country_df = df[df['location'] == query['country']]

    country = query['country']

    vars1 = {label: var1 for label, var1 in zip(country_df.index.to_list(), country_df[var1].fillna('pad').to_list())}
    vars2 = {label: var2 for label, var2 in zip(country_df.index.to_list(), country_df[var2].fillna('pad').to_list())}

    return JsonResponse(data={"query_var_1": parse_var(var1),
                              "query_var_2": parse_var(var2),
                              "country": country,
                              "vars1": vars1,
                              "vars2": vars2})

