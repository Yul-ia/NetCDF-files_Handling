import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from decimal import Decimal, ROUND_HALF_UP
import pymannkendall as mk
from dateutil.relativedelta import relativedelta

os.chdir('')

## air_ anorm df
anom_path = '6.anom_std_csv/'
air_anom_new = pd.read_csv(anom_path + 'air_anom_std_new.csv')
prate_anom_new = pd.read_csv(anom_path + 'prate_anom_std_new.csv')
pres_anom_new = pd.read_csv(anom_path + 'pres_anom_std_new.csv')
wind_anom_new = pd.read_csv(anom_path + 'wind_anom_std_new.csv')

### data type change todatetime
def change_type(df_name):
    df_name['date'] = pd.to_datetime(df_name['date'], format='%Y-%m-%d')

# (df_name,area,star_year=int(),end_year=int()+1)
def decade_trend(df_name,area,star_year=int(),end_year=int()+1):
    trend_df= pd.DataFrame(columns=['year','jan_trend','feb_tren', 'mar_trend','apr_trend',
                                        'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for start_year in range(star_year, end_year, 10):
        end_year = start_year + 9
        decade_df = df_name[(df_name['date'].dt.year >= start_year) & (df_name['date'].dt.year <= end_year)]
        
        date_name = f"{start_year}-{end_year}"
        row_data = {'year': date_name}
        
        for i in range(1, 13):
            month= decade_df[decade_df['date'].dt.month == i]
            
            if len(month) > 0:
                man = mk.original_test(month[area])
                row_data[trend_df.columns[i]] = man.slope
                
        trend_df = pd.concat([trend_df, pd.DataFrame([row_data])], ignore_index=True)
    return trend_df

#%%
df_lst = [air_anom_new, prate_anom_new, pres_anom_new, wind_anom_new]
var_lst = ['air','prate','pres','wind']

area_lst = ['glb_anom','ask_anom', 'es_anom', 'ys_anom', 'ecs_anom']

new_df_name = ['glb_decadal_trend','ask_decadal_trend', 'es_decadal_trend', 'ys_decadal_trend', 'ecs_decadal_trend']

## change data type
for df in df_lst:
    change_type(df)


air_glb_decadal_trend = decade_trend(air_anom_new, 'glb_anom', 1991, 2020)
air_ask_decadal_trend = decade_trend(air_anom_new, 'ask_anom', 1991, 2020)
air_es_decadal_trend = decade_trend(air_anom_new, 'es_anom', 1991, 2020)
air_ys_decadal_trend = decade_trend(air_anom_new, 'ys_anom', 1991, 2020)
air_ecs_decadal_trend = decade_trend(air_anom_new, 'ecs_anom', 1991, 2020)

prate_glb_decadal_trend = decade_trend(prate_anom_new, 'glb_anom', 1991, 2020)
prate_ask_decadal_trend = decade_trend(prate_anom_new, 'ask_anom', 1991, 2020)
prate_es_decadal_trend = decade_trend(prate_anom_new, 'es_anom', 1991, 2020)
prate_ys_decadal_trend = decade_trend(prate_anom_new, 'ys_anom', 1991, 2020)
prate_ecs_decadal_trend = decade_trend(prate_anom_new, 'ecs_anom', 1991, 2020)

pres_glb_decadal_trend = decade_trend(pres_anom_new, 'glb_anom', 1991, 2020)
pres_ask_decadal_trend = decade_trend(pres_anom_new, 'ask_anom', 1991, 2020)
pres_es_decadal_trend = decade_trend(pres_anom_new, 'es_anom', 1991, 2020)
pres_ys_decadal_trend = decade_trend(pres_anom_new, 'ys_anom', 1991, 2020)
pres_ecs_decadal_trend = decade_trend(pres_anom_new, 'ecs_anom', 1991, 2020)

wind_glb_decadal_trend = decade_trend(wind_anom_new, 'glb_anom', 1991, 2020)
wind_ask_decadal_trend = decade_trend(wind_anom_new, 'ask_anom', 1991, 2020)
wind_es_decadal_trend = decade_trend(wind_anom_new, 'es_anom', 1991, 2020)
wind_ys_decadal_trend = decade_trend(wind_anom_new, 'ys_anom', 1991, 2020)
wind_ecs_decadal_trend = decade_trend(wind_anom_new, 'ecs_anom', 1991, 2020)



# round df
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


os.getcwd()
air_glb_decadal_trend.to_csv('air_glb_decadal_trend_new_MK.csv',index=False)
air_ask_decadal_trend.to_csv('air_ask_decadal_trend_new_MK.csv',index=False)
air_es_decadal_trend.to_csv('air_es_decadal_trend_new_MK.csv',index=False)
air_ys_decadal_trend.to_csv('air_ys_decadal_trend_new_MK.csv',index=False)
air_ecs_decadal_trend.to_csv('air_ecs_decadal_trend_new_MK.csv',index=False)

prate_glb_decadal_trend.to_csv('prate_glb_decadal_trend_new_MK.csv',index=False)
prate_ask_decadal_trend.to_csv('prate_ask_decadal_trend_new_MK.csv',index=False)
prate_es_decadal_trend.to_csv('prate_es_decadal_trend_new_MK.csv',index=False)
prate_ys_decadal_trend.to_csv('prate_ys_decadal_trend_new_MK.csv',index=False)
prate_ecs_decadal_trend.to_csv('prate_ecs_decadal_trend_new_MK.csv',index=False)

pres_glb_decadal_trend.to_csv('pres_glb_decadal_trend_new_MK.csv',index=False)
pres_ask_decadal_trend.to_csv('pres_ask_decadal_trend_new_MK.csv',index=False)
pres_es_decadal_trend.to_csv('pres_es_decadal_trend_new_MK.csv',index=False)
pres_ys_decadal_trend.to_csv('pres_ys_decadal_trend_new_MK.csv',index=False)
pres_ecs_decadal_trend.to_csv('pres_ecs_decadal_trend_new_MK.csv',index=False)

wind_glb_decadal_trend.to_csv('wind_glb_decadal_trend_new_MK.csv',index=False)
wind_ask_decadal_trend.to_csv('wind_ask_decadal_trend_new_MK.csv',index=False)
wind_es_decadal_trend.to_csv('wind_es_decadal_trend_new_MK.csv',index=False)
wind_ys_decadal_trend.to_csv('wind_ys_decadal_trend_new_MK.csv',index=False)
wind_ecs_decadal_trend.to_csv('wind_ecs_decadal_trend_new_MK.csv',index=False)


