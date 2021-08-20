import os
import time
import datetime

from covidgraphs.constants import COVID_DATA_FILE
from covidgraphs.templatetags.filter import register

@register.inclusion_tag('covidgraphs/last_modified.html')
def last_modified():
    t = os.path.getmtime(COVID_DATA_FILE)

    return {"last_modified":datetime.datetime.fromtimestamp(t)}

