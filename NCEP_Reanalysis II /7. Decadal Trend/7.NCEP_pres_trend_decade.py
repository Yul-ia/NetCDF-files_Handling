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

def decade_trend(area):
    trend_df= pd.DataFrame(columns=['year','jan_trend','feb_tren', 'mar_trend','apr_trend',
                                        'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for start_year in range(1991, 2021, 10):
        end_year = start_year + 9
        decade_df = pres_anom[(pres_anom['date'].dt.year >= start_year) & (pres_anom['date'].dt.year <= end_year)]
        
        col_name = f"{start_year}-{end_year}"
        row_data = {'year': col_name}
        
        for i in range(1, 13):
            month= decade_df[decade_df['date'].dt.month == i]
            
            if len(month) > 0:
                anom_values = month[area].values
                x = np.arange(len(anom_values))
                
                a, b = np.polyfit(x, anom_values, deg=1)
                row_data[trend_df.columns[i]] = a / 10  # Divide into decades
            else:
                row_data[trend_df.columns[i]] = np.nan  # NaN handling
        

        trend_df = trend_df.append(row_data, ignore_index=True)
    return trend_df

change_type(pres_anom)

pres_glb_decadal_trend = decade_trend('glb_anom')
pres_ask_decadal_trend = decade_trend('ask_anom')
pres_es_decadal_trend = decade_trend('es_anom')
pres_ys_decadal_trend = decade_trend('ys_anom')
pres_ecs_decadal_trend = decade_trend('ecs_anom')

os.getcwd()

pres_glb_decadal_trend.to_csv('pres_glb_decadal_trend_new.csv',index=False)
pres_ask_decadal_trend.to_csv('pres_ask_decadal_trend_new.csv',index=False)
pres_es_decadal_trend.to_csv('pres_es_decadal_trend_new.csv',index=False)
pres_ys_decadal_trend.to_csv('pres_ys_decadal_trend_new.csv',index=False)
pres_ecs_decadal_trend.to_csv('pres_ecs_decadal_trend_new.csv',index=False)
