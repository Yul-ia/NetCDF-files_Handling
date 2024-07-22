import os
import pandas as pd
import numpy as np
import xarray as xr
import datetime
import pymannkendall as mk
from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta

os.chdir('')
precip_anom = pd.read_csv('6.CMAP_anom_std_csv/precip_anom_std_old.csv')

### data type change todatetime
def change_type(df_name):
    df_name['date'] = pd.to_datetime(df_name['date'], format='%Y-%m-%d')
    
    
def decade_trend(area):
    trend_df= pd.DataFrame(columns=['year','jan_trend','feb_tren', 'mar_trend','apr_trend',
                                        'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for start_year in range(1991, 2021, 10):
        end_year = start_year + 9
        decade_df = precip_anom[(precip_anom['date'].dt.year >= start_year) & (precip_anom['date'].dt.year <= end_year)]
        
        date_name = f"{start_year}-{end_year}"
        row_data = {'year': date_name}
        
        for i in range(1, 13):
            month= decade_df[decade_df['date'].dt.month == i]
            
            if len(month) > 0:
                man = mk.original_test(month[area])
                row_data[trend_df.columns[i]] = man.slope
                # row_data[trend_df.columns[i]] = man.p

        # trend_df = trend_df.append(row_data, ignore_index=True) # version error
        trend_df = pd.concat([trend_df, pd.DataFrame([row_data])], ignore_index=True)

    return trend_df



## apply
change_type(precip_anom)
precip_glb_decadal_trend = decade_trend('glb_anom')
precip_ask_decadal_trend = decade_trend('ask_anom')
precip_es_decadal_trend = decade_trend('es_anom')
precip_ys_decadal_trend = decade_trend('ys_anom')
precip_ecs_decadal_trend = decade_trend('ecs_anom')

precip_glb_decadal_trend.to_csv('precip_glb_decadal_trend_old_MK.csv',index=False)
precip_ask_decadal_trend.to_csv('precip_ask_decadal_trend_old_MK.csv',index=False)
precip_es_decadal_trend.to_csv('precip_es_decadal_trend_old_MK.csv',index=False)
precip_ys_decadal_trend.to_csv('precip_ys_decadal_trend_old_MK.csv',index=False)
precip_ecs_decadal_trend.to_csv('precip_ecs_decadal_trend_old_MK.csv',index=False)
