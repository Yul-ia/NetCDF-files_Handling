import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime

os.chdir('')

## wind_ anorm df
anom_path = 'anom_csv/'
wind_anom = pd.read_csv(anom_path + 'wind_anom_new.csv')

### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')


def trend (area):
    trend_df= pd.DataFrame(columns=['jan_trend','feb_tren', 'mar_trend','apr_trend',
                                      'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for i in range(1,13):
        mon = wind_anom[wind_anom['date'].dt.month == i]
        mon_values = mon[area].values
        x = np.arange(len(mon_values))
        a,b = np.polyfit(x,mon_values,deg=1)
        trend_df.loc[0, trend_df.columns[i-1]] = a/10

    trend_df.reset_index(drop=True,inplace=True)
    return trend_df

change_type(wind_anom)

wind_glb_trend = trend('glb_anom')
wind_ask_trend = trend('ask_anom')
wind_es_trend = trend('es_anom')
wind_ys_trend = trend('ys_anom')
wind_ecs_trend = trend('ecs_anom')

os.getcwd()
wind_glb_trend.to_csv('wind_glb_trend_new.csv',index=False)
wind_ask_trend.to_csv('wind_ask_trend_new.csv',index=False)
wind_es_trend.to_csv('wind_es_trend_new.csv',index=False)
wind_ys_trend.to_csv('wind_ys_trend_new.csv',index=False)
wind_ecs_trend.to_csv('wind_ecs_trend_new.csv',index=False)
