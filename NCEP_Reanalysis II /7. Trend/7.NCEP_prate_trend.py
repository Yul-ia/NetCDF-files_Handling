import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime

os.chdir('')

## prate_ anorm df
anom_path = 'anom_csv/'
prate_anom = pd.read_csv(anom_path + 'prate_anom_new.csv')

### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')


def trend (area):
    trend_df= pd.DataFrame(columns=['jan_trend','feb_tren', 'mar_trend','apr_trend',
                                      'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for i in range(1,13):
        mon = prate_anom[prate_anom['date'].dt.month == i]
        mon_values = mon[area].values
        x = np.arange(len(mon_values))
        a,b = np.polyfit(x,mon_values,deg=1)
        # prate_anom['trend_%s' %i] == a/10 ## 기존 csv에 저장할 경우.
        trend_df.loc[0, trend_df.columns[i-1]] = a/10

    trend_df.reset_index(drop=True,inplace=True)
    return trend_df

change_type(prate_anom)

prate_glb_trend = trend('glb_anom')
prate_ask_trend = trend('ask_anom')
prate_es_trend = trend('es_anom')
prate_ys_trend = trend('ys_anom')
prate_ecs_trend = trend('ecs_anom')

os.getcwd()
prate_glb_trend.to_csv('prate_glb_trend_new.csv',index=False)
prate_ask_trend.to_csv('prate_ask_trend_new.csv',index=False)
prate_es_trend.to_csv('prate_es_trend_new.csv',index=False)
prate_ys_trend.to_csv('prate_ys_trend_new.csv',index=False)
prate_ecs_trend.to_csv('prate_ecs_trend_new.csv',index=False)
