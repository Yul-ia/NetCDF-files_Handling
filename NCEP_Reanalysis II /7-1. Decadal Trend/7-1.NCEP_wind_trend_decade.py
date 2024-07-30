import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime

os.chdir('')

## wind_ anorm df
anom_path = 'anom_std_csv/'
wind_anom = pd.read_csv(anom_path + 'wind_anom_std_new.csv')

### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')


def decade_trend(area):
    trend_df= pd.DataFrame(columns=['year','jan_trend','feb_tren', 'mar_trend','apr_trend',
                                        'may_trend' ,'jun_trend' ,'jul_trend','aug_trend','sep_trend','oct_trend','nov_trend','dec_trend'])

    for start_year in range(1991, 2021, 10):
        end_year = start_year + 9
        decade_df = wind_anom[(wind_anom['date'].dt.year >= start_year) & (wind_anom['date'].dt.year <= end_year)]
        
        col_name = f"{start_year}-{end_year}"
        row_data = {'year': col_name}
        
        for i in range(1, 13):
            month= decade_df[decade_df['date'].dt.month == i]
            
            if len(month) > 0:
                anom_values = month[area].values
                x = np.arange(len(anom_values))
                
                a, b = np.polyfit(x, anom_values, deg=1)
                row_data[trend_df.columns[i]] = a / 10  # 10년 단위로 나누기
            else:
                row_data[trend_df.columns[i]] = np.nan  # 데이터가 없는 경우 NaN 처리
        

        trend_df = trend_df.append(row_data, ignore_index=True)
    return trend_df


def round_up(num):
    result = Decimal(num).quantize(Decimal('.00'),rounding=ROUND_HALF_UP)
    return result

def round_up_df(df_name):
    df_cols = df_name.select_dtypes(include=['float64', 'int64']).columns
    df_name[df_cols] = df_name[df_cols].applymap(round_up)


change_type(wind_anom)

wind_glb_decadal_trend = decade_trend('glb_anom')
wind_ask_decadal_trend = decade_trend('ask_anom')
wind_es_decadal_trend = decade_trend('es_anom')
wind_ys_decadal_trend = decade_trend('ys_anom')
wind_ecs_decadal_trend = decade_trend('ecs_anom')
     
# round_up_df(wind_glb_decadal_trend)
# round_up_df(wind_ask_decadal_trend)
# round_up_df(wind_es_decadal_trend)
# round_up_df(wind_ecs_decadal_trend)

os.getcwd()
# wind_glb_decadal_trend.to_csv('wind_glb_decadal_trend_new.csv',index=False)
# wind_ask_decadal_trend.to_csv('wind_ask_decadal_trend_new.csv',index=False)
# wind_es_decadal_trend.to_csv('wind_es_decadal_trend_new.csv',index=False)
# wind_ys_decadal_trend.to_csv('wind_ys_decadal_trend_new.csv',index=False)
# wind_ecs_decadal_trend.to_csv('wind_ecs_decadal_trend_new.csv',index=False)
