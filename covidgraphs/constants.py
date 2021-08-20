import os
DATA_DIR = './data'
os.makedirs(DATA_DIR,exist_ok=True)
COVID_DATA_FILE = os.path.join(DATA_DIR,'covid_data.csv')
LAST_CHECK_FILE = os.path.join(DATA_DIR,'last_check.txt')

LAST_UPDATE_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data-last-updated-timestamp.txt"
COVID_DATA_URL='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
