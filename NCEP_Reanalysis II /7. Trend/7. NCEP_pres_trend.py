import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime

os.chdir('')

## pres_ anorm df
anom_path = 'anom_csv/'
pres_anom = pd.read_csv(anom_path + 'pres_anom_new.csv')

### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')

def trend (area):
    trend_df= pd.DataFrame(columns=['jan_trend','feb_tren', 'mar_trend','apr_trend',
                                      'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for i in range(1,13):
        mon = pres_anom[pres_anom['date'].dt.month == i]
        mon_values = mon[area].values
        x = np.arange(len(mon_values))
        a,b = np.polyfit(x,mon_values,deg=1)
        trend_df.loc[0, trend_df.columns[i-1]] = a/10

    trend_df.reset_index(drop=True,inplace=True)
    return trend_df

change_type(pres_anom)

pres_glb_trend = trend('glb_anom')
pres_ask_trend = trend('ask_anom')
pres_es_trend = trend('es_anom')
pres_ys_trend = trend('ys_anom')
pres_ecs_trend = trend('ecs_anom')

os.getcwd()
pres_glb_trend.to_csv('pres_glb_trend_new.csv',index=False)
pres_ask_trend.to_csv('pres_ask_trend_new.csv',index=False)
pres_es_trend.to_csv('pres_es_trend_new.csv',index=False)
pres_ys_trend.to_csv('pres_ys_trend_new.csv',index=False)
pres_ecs_trend.to_csv('pres_ecs_trend_new.csv',index=False)
