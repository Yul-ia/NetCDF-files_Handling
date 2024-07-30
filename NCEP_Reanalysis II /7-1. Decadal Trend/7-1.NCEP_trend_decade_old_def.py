import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from decimal import Decimal, ROUND_HALF_UP

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
                y = month[area].values
                x = np.arange(len(y))
                
                a, b = np.polyfit(x, y, deg=1)
                row_data[trend_df.columns[i]] = a 
            else:
                row_data[trend_df.columns[i]] = np.nan 
        

        trend_df = trend_df.append(row_data, ignore_index=True)
    return trend_df

# round def
def round_up(num):
    result = Decimal(num).quantize(Decimal('.00'),rounding=ROUND_HALF_UP)
    return result

def round_up_df(df_name):
    df_cols = df_name.select_dtypes(include=['float64', 'int64']).columns
    df_name[df_cols] = df_name[df_cols].applymap(round_up)
    

#%%
os.chdir('d://NCEP_R2')
## air_ anorm df
anom_path = '6.anom_std_csv/'
air_anom_old = pd.read_csv(anom_path + 'air_anom_std_old.csv')
prate_anom_old = pd.read_csv(anom_path + 'prate_anom_std_old.csv')
pres_anom_old = pd.read_csv(anom_path + 'pres_anom_std_old.csv')
wind_anom_old = pd.read_csv(anom_path + 'wind_anom_std_old.csv')

#%%
df_lst = [air_anom_old, prate_anom_old, pres_anom_old, wind_anom_old]
var_lst = ['air','prate','pres','wind']

area_lst = ['glb_anom','ask_anom', 'es_anom', 'ys_anom', 'ecs_anom']

new_df_name = ['glb_decadal_trend','ask_decadal_trend', 'es_decadal_trend', 'ys_decadal_trend', 'ecs_decadal_trend']

## change data type
for df in df_lst:
    change_type(df)


air_glb_decadal_trend = decade_trend(air_anom_old, 'glb_anom', 1981, 2010)
air_ask_decadal_trend = decade_trend(air_anom_old, 'ask_anom', 1981, 2010)
air_es_decadal_trend = decade_trend(air_anom_old, 'es_anom', 1981, 2010)
air_ys_decadal_trend = decade_trend(air_anom_old, 'ys_anom', 1981, 2010)
air_ecs_decadal_trend = decade_trend(air_anom_old, 'ecs_anom', 1981, 2010)

prate_glb_decadal_trend = decade_trend(prate_anom_old, 'glb_anom', 1981, 2010)
prate_ask_decadal_trend = decade_trend(prate_anom_old, 'ask_anom', 1981, 2010)
prate_es_decadal_trend = decade_trend(prate_anom_old, 'es_anom', 1981, 2010)
prate_ys_decadal_trend = decade_trend(prate_anom_old, 'ys_anom', 1981, 2010)
prate_ecs_decadal_trend = decade_trend(prate_anom_old, 'ecs_anom', 1981, 2010)

pres_glb_decadal_trend = decade_trend(pres_anom_old, 'glb_anom', 1981, 2010)
pres_ask_decadal_trend = decade_trend(pres_anom_old, 'ask_anom', 1981, 2010)
pres_es_decadal_trend = decade_trend(pres_anom_old, 'es_anom', 1981, 2010)
pres_ys_decadal_trend = decade_trend(pres_anom_old, 'ys_anom', 1981, 2010)
pres_ecs_decadal_trend = decade_trend(pres_anom_old, 'ecs_anom', 1981, 2010)

wind_glb_decadal_trend = decade_trend(wind_anom_old, 'glb_anom', 1981, 2010)
wind_ask_decadal_trend = decade_trend(wind_anom_old, 'ask_anom', 1981, 2010)
wind_es_decadal_trend = decade_trend(wind_anom_old, 'es_anom', 1981, 2010)
wind_ys_decadal_trend = decade_trend(wind_anom_old, 'ys_anom', 1981, 2010)
wind_ecs_decadal_trend = decade_trend(wind_anom_old, 'ecs_anom', 1981, 2010)


# ###################################
# trend_dict = {}
# # decadal trend 계산 및 딕셔너리에 저장
# for df, var in zip(df_lst, var_lst):
#     for area, new_df in zip(area_lst, new_df_name):
#         trend_name = f'{var}_{new_df}'
#         trend_dict[trend_name] = decade_trend(df, area, 1981, 2010)

# # 예: trend_dict 딕셔너리에 저장된 데이터프레임 접근
# for trend_name, trend_data in trend_dict.items():
#     print(f"{trend_name}:")
#     print(trend_data.head())

#################################

      
# round_up_df(air_glb_decadal_trend)
# round_up_df(air_ask_decadal_trend)
# round_up_df(air_es_decadal_trend)
# round_up_df(air_ecs_decadal_trend)


os.getcwd()
# air_glb_decadal_trend.to_csv('air_glb_decadal_trend_old.csv',index=False)
# air_ask_decadal_trend.to_csv('air_ask_decadal_trend_old.csv',index=False)
# air_es_decadal_trend.to_csv('air_es_decadal_trend_old.csv',index=False)
# air_ys_decadal_trend.to_csv('air_ys_decadal_trend_old.csv',index=False)
# air_ecs_decadal_trend.to_csv('air_ecs_decadal_trend_old.csv',index=False)

# prate_glb_decadal_trend.to_csv('prate_glb_decadal_trend_old.csv',index=False)
# prate_ask_decadal_trend.to_csv('prate_ask_decadal_trend_old.csv',index=False)
# prate_es_decadal_trend.to_csv('prate_es_decadal_trend_old.csv',index=False)
# prate_ys_decadal_trend.to_csv('prate_ys_decadal_trend_old.csv',index=False)
# prate_ecs_decadal_trend.to_csv('prate_ecs_decadal_trend_old.csv',index=False)

# pres_glb_decadal_trend.to_csv('pres_glb_decadal_trend_old.csv',index=False)
# pres_ask_decadal_trend.to_csv('pres_ask_decadal_trend_old.csv',index=False)
# pres_es_decadal_trend.to_csv('pres_es_decadal_trend_old.csv',index=False)
# pres_ys_decadal_trend.to_csv('pres_ys_decadal_trend_old.csv',index=False)
# pres_ecs_decadal_trend.to_csv('pres_ecs_decadal_trend_old.csv',index=False)

# wind_glb_decadal_trend.to_csv('wind_glb_decadal_trend_old.csv',index=False)
# wind_ask_decadal_trend.to_csv('wind_ask_decadal_trend_old.csv',index=False)
# wind_es_decadal_trend.to_csv('wind_es_decadal_trend_old.csv',index=False)
# wind_ys_decadal_trend.to_csv('wind_ys_decadal_trend_old.csv',index=False)
# wind_ecs_decadal_trend.to_csv('wind_ecs_decadal_trend_old.csv',index=False)

