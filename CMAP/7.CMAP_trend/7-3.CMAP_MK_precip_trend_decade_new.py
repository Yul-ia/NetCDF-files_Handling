import os
import pandas as pd
import numpy as np
import xarray as xr
import datetime
import pymannkendall as mk
from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta

os.chdir('')
precip_anom = pd.read_csv('6.CMAP_anom_std_csv/precip_anom_std_new.csv')

precip_anom.drop('unit',axis = 1, inplace=True)


### data type change todatetime
def change_type(df_name):
    df_name['date'] = pd.to_datetime(df_name['date'], format='%Y-%m-%d')
    
    
def decade_trend(area):
    trend_df= pd.DataFrame(columns=['year','jan_trend','jan_p_value','feb_trend','feb_p_value', 'mar_trend','mar_p_value','apr_trend','apr_p_value',
                                        'may_trend','may_p_value' ,'jun_trend' ,'jun_p_value','jul_trend','jul_p_value','aug_trend','aug_p_value',
                                        'sep_trend','sep_p_value','oct_trend','oct_p_value','nov_trend','nov_p_value','dec_trend','dec_p_value'])
    for start_year in range(1991, 2021, 10):
        end_year = start_year + 9
        decade_df = precip_anom[(precip_anom['date'].dt.year >= start_year) & (precip_anom['date'].dt.year <= end_year)]
        
        date_name = f"{start_year}-{end_year}"
        row_data = {'year': date_name}
        
        for i in range(1,13):
            month= decade_df[decade_df['date'].dt.month == i]

            odd= (i - 1) * 2 + 1  
            even = (i - 1) * 2 + 2 
            
            if not month.empty and len(month[area].unique()) > 1:
                man = mk.original_test(month[area])
                row_data[trend_df.columns[odd]] = man.slope
                row_data[trend_df.columns[even]] = man.p
            else:
                row_data[trend_df.columns[odd]] = np.nan
                row_data[trend_df.columns[even]] = np.nan
        trend_df = pd.concat([trend_df, pd.DataFrame([row_data])], ignore_index=True)

    return trend_df

## apply
change_type(precip_anom)


precip_glb_decadal_trend = decade_trend('glb_anom')
precip_ask_decadal_trend = decade_trend('ask_anom')
precip_es_decadal_trend = decade_trend('es_anom')
precip_ys_decadal_trend = decade_trend('ys_anom')
precip_ecs_decadal_trend = decade_trend('ecs_anom')

precip_glb_decadal_trend.to_csv('precip_glb_decadal_trend_new_MK.csv',index=False)
precip_ask_decadal_trend.to_csv('precip_ask_decadal_trend_new_MK.csv',index=False)
precip_es_decadal_trend.to_csv('precip_es_decadal_trend_new_MK.csv',index=False)
precip_ys_decadal_trend.to_csv('precip_ys_decadal_trend_new_MK.csv',index=False)
precip_ecs_decadal_trend.to_csv('precip_ecs_decadal_trend_new_MK.csv',index=False)
