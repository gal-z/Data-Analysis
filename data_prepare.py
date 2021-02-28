import pandas as pd
import re
import datetime



data_apps = pd.read_csv("apps.csv", encoding="ISO-8859-1")
data_user_reviews = pd.read_csv("user_reviews.csv", encoding="ISO-8859-1")

def change_coll_only_num(coll):
    app_size = []
    for i in coll:
       i=re.sub('M','000000',i)
       i = re.sub('k', '000', i)
       i=re.sub("Varies with device","0",i)
       if int((float(i)))!=float(i):
        i= float(i)*1000000000
       i=int(float(i))
       if i <10:
           i=i*1000000000
       app_size.append(i)
    coll=app_size
    return coll


def clean_install_coll(install_coull):
    data_apps_download = install_coull.str.replace('+', '')
    data_apps_download_new = data_apps_download.str.replace(',', '').astype(int)
    return data_apps_download_new

def change_time (date_index):
    date_time_str = date_index
    date_time_obj = datetime.datetime.strptime(date_time_str, '%B %d, %Y')
    return date_time_obj


def change_app_coll_nan(data_coll):
    pta = pd.Series(data_coll)
    pta[pta.isnull()]= 'has_no_name'
    return pta

def change_rating_coll_nan(data_coll):
    pto = pd.Series(data_coll)
    pto[pto.isnull()]=0
    return pto

def clean_nan_from_sentiment_subj(data):
    pta = pd.Series(data)
    pta[pta.isnull()]= pta.mean()
    return pta


def clean_nan_from_sentiment_pol(data):
    ptb = pd.Series(data)
    ptb[ptb.isnull()]= ptb.mean()
    return ptb

def insert_most_frequent_to_nan_sentiment(data):
    ptc = pd.Series(data)
    mode = ptc.mode()
    ptc[ptc.isnull()]= 'Positive'
    return ptc