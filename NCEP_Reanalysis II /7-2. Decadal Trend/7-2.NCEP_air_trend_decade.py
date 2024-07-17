import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from decimal import Decimal, ROUND_HALF_UP

os.chdir('')

## air_ anorm df
anom_path = 'anom_std_csv/'
air_anom = pd.read_csv(anom_path + 'air_anom_std_new.csv')

### data type change todatetime
def change_type(df_name):
    df_name['date'] = pd.to_datetime(df_name['date'], format='%Y-%m-%d')


def decade_trend(area):
    trend_df= pd.DataFrame(columns=['year','jan_trend','feb_tren', 'mar_trend','apr_trend',
                                        'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for start_year in range(1991, 2021, 10):
        end_year = start_year + 9
        decade_df = air_anom[(air_anom['date'].dt.year >= start_year) & (air_anom['date'].dt.year <= end_year)]
        
        date_name = f"{start_year}-{end_year}"
        row_data = {'year': date_name}
        
        for i in range(1, 13):
            month= decade_df[decade_df['date'].dt.month == i]
            
            if len(month) > 0:
                y = month[area].values
                x = np.arange(len(y))
                
                a, b = np.polyfit(x, y, deg=1)
                row_data[trend_df.columns[i]] = a 
            else:
                row_data[trend_df.columns[i]] = np.nan 
        

        trend_df = trend_df.append(row_data, ignore_index=True)
    return trend_df


change_type(air_anom)

air_glb_decadal_trend = decade_trend('glb_anom')
air_ask_decadal_trend = decade_trend('ask_anom')
air_es_decadal_trend = decade_trend('es_anom')
air_ys_decadal_trend = decade_trend('ys_anom')
air_ecs_decadal_trend = decade_trend('ecs_anom')

# air_glb_trend=air_glb_trend.round(2)

## round def
def round_up(num):
    result = Decimal(num).quantize(Decimal('.00'),rounding=ROUND_HALF_UP)
    return result

def round_up_df(df_name):
    df_cols = df_name.select_dtypes(include=['float64', 'int64']).columns
    df_name[df_cols] = df_name[df_cols].applymap(round_up)
       
# round_up_df(air_glb_decadal_trend)
# round_up_df(air_ask_decadal_trend)
# round_up_df(air_es_decadal_trend)
# round_up_df(air_ecs_decadal_trend)

# os.getcwd()
air_glb_decadal_trend.to_csv('air_glb_decadal_trend_new.csv',index=False)
air_ask_decadal_trend.to_csv('air_ask_decadal_trend_new.csv',index=False)
air_es_decadal_trend.to_csv('air_es_decadal_trend_new.csv',index=False)
air_ys_decadal_trend.to_csv('air_ys_decadal_trend_new.csv',index=False)
air_ecs_decadal_trend.to_csv('air_ecs_decadal_trend_new.csv',index=False)


