import os
from functools import lru_cache
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from pandas import DataFrame

from covidgraphs.templatetags.filter import parse_var
from .constants import DATA_DIR
from update_database import get_newest_data


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

