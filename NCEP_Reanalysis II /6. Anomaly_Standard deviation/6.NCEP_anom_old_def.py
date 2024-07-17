import os
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from decimal import Decimal, ROUND_HALF_UP

os.chdir('')

## average monthly values per year
path = 'east_asia_weighted/'
air_mean = pd.read_csv(path+'air_asia_mask&weighted.csv')
prate_mean = pd.read_csv(path+ 'prate_asia_mask&weighted.csv')
pres_mean = pd.read_csv(path + 'pres_asia_mask&weighted.csv')
wind_mean = pd.read_csv(path + 'wind_asia_mask&weighted.csv')

## new climate
clim_path = 'longterm_asia_weighted_csv/'
air_clim = pd.read_csv(clim_path + 'air_old_longterm_east_asia_mask&weight.csv')
prate_clim = pd.read_csv(clim_path+'prate_old_longterm_east_asia_mask&weight.csv')
pres_clim = pd.read_csv(clim_path+'pres_old_longterm_east_asia_mask&weight.csv')
wind_clim = pd.read_csv(clim_path+'wind_old_longterm_east_asia_mask&weighted.csv')


### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')

def anom_df(df_name,clim_df):
    df_name['month']=df_name['date'].dt.month
    df_name['year']= df_name['date'].dt.year
    df_name=df_name.loc[df_name['year'].between(1981,2010)] # new_clim

    df_name.sort_values(by=['year','month'],ascending=[True,True],inplace=True)

    # climate average application
    for i in range(1, 13):
        mon = df_name['date'].dt.month == i
        df_name.loc[mon, 'glb_clim'] = clim_df.loc[clim_df['month'] == i, 'glb_clim'].values[0]
        df_name.loc[mon, 'ask_clim'] = clim_df.loc[clim_df['month'] == i, 'ask_clim'].values[0]
        df_name.loc[mon, 'es_clim'] = clim_df.loc[clim_df['month'] == i, 'es_clim'].values[0]
        df_name.loc[mon, 'ys_clim'] = clim_df.loc[clim_df['month'] == i, 'ys_clim'].values[0]
        df_name.loc[mon, 'ecs_clim'] = clim_df.loc[clim_df['month'] == i, 'ecs_clim'].values[0]
        
        df_name.loc[mon, 'glb_std'] = df_name.loc[df_name['month']==i,'glb_mean'].std() # ddof=0
        df_name.loc[mon, 'ask_std'] = df_name.loc[df_name['month']==i,'ask_mean'].std()
        df_name.loc[mon, 'es_std'] = df_name.loc[df_name['month']==i,'es_mean'].std()
        df_name.loc[mon, 'ys_std'] = df_name.loc[df_name['month']==i,'ys_mean'].std()
        df_name.loc[mon, 'ecs_std'] = df_name.loc[df_name['month']==i,'ecs_mean'].std()

    # anomaly appllication
    for idx, row in df_name.iterrows():
        df_name.loc[idx, 'glb_anom'] = row['glb_mean'] - row['glb_clim']
        df_name.loc[idx, 'ask_anom'] = row['ask_mean'] - row['ask_clim']
        df_name.loc[idx, 'es_anom'] = row['es_mean'] - row['es_clim']
        df_name.loc[idx, 'ys_anom'] = row['ys_mean'] - row['ys_clim']
        df_name.loc[idx, 'ecs_anom'] = row['ecs_mean'] - row['ecs_clim']

    df_name.drop(['month','year'], axis=1, inplace=True)
    df_name.reset_index(drop=True)

    df_name=df_name[['date', 'glb_mean', 'glb_clim', 'glb_anom','glb_std','ask_mean', 'ask_clim', 'ask_anom','ask_std','es_mean',
       'es_clim', 'es_anom','es_std', 'ys_mean', 'ys_clim','ys_anom', 'ys_std','ecs_mean', 'ecs_clim', 'ecs_anom','ecs_std']]
    
    df_name.reset_index(drop=True,inplace=True)
    
    return df_name

## apply def
change_type(air_mean)
change_type(prate_mean)
change_type(pres_mean)
change_type(wind_mean)

air_mean = anom_df(air_mean,air_clim)
prate_mean = anom_df(prate_mean,prate_clim)
pres_mean = anom_df(pres_mean,pres_clim)
wind_mean = anom_df(wind_mean,wind_clim)

air_mean['unit'] = 'deg C'
prate_mean['unit'] = 'mm'
pres_mean['unit'] = 'hPa'
wind_mean['unit'] = 'm/s'


# round def
def round_up(num):
    result = Decimal(num).quantize(Decimal('.00'),rounding=ROUND_HALF_UP)
    return result

def round_up_df(df_name):
    df_cols = df_name.select_dtypes(include=['float64', 'int64']).columns
    df_name[df_cols] = df_name[df_cols].applymap(round_up)
          
# round_up_df(air_mean)
# round_up_df(prate_mean)
# round_up_df(pres_mean)
# round_up_df(wind_mean)


os.getcwd()

# air_mean.to_csv('air_anom_old.csv',index=False)
# prate_mean.to_csv('prate_anom_old.csv',index=False)
# pres_mean.to_csv('pres_anom_old.csv',index=False)
# wind_mean.to_csv('wind_anom_old.csv',index=False)
