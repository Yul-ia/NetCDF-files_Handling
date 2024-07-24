# 6.CMAP_anom_std_new.py
import os
import numpy as np
import pandas as pd
import xarray as xr
from decimal import Decimal, ROUND_HALF_UP
from dateutil.relativedelta import relativedelta

os.chdir('')

##average monthly values per year
path = '4.CMAP_weighted/'
precip_mean = pd.read_csv(path+'precip_asia_mask&weighted.csv')

## clim df
clim_path = '5.CMAP_longterm_asia_weighted_csv/'
precip_clim = pd.read_csv(clim_path + 'precip_new_lonterm_east_asia_mask&weighted.csv') # new climate
precip_clim_old = pd.read_csv(clim_path + 'precip_old_lonterm_east_asia_mask&weighted.csv') # old climate

### data type change todatetime
def change_type(col_name):
    col_name['date'] = pd.to_datetime(col_name['date'], format='%Y-%m-%d')

def anom_df(df_name,clim_df,start_year=int(), end_year=int()):
    df_name['month']=df_name['date'].dt.month
    df_name['year']= df_name['date'].dt.year
    df_name=df_name.loc[df_name['year'].between(start_year,end_year)] # new_clim

    # df_name.sort_values(by=['month','year'],ascending=[True,True],inplace=True)## month - year
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

# round def
def round_up(num):
    result = Decimal(num).quantize(Decimal('.00'),rounding=ROUND_HALF_UP)
    return result

def round_up_df(df_name):
    df_cols = df_name.select_dtypes(include=['float64', 'int64']).columns
    df_name[df_cols] = df_name[df_cols].applymap(round_up)



## apply def
change_type(precip_mean)
precip_mean_new =  anom_df(precip_mean,precip_clim, 1991 ,2020) # new_df
precip_mean_old = anom_df(precip_mean,precip_clim_old, 1981 ,2010) # old_df

precip_mean_new['unit'] = 'mm/month'
precip_mean_old['unit'] = 'mm/month'


    
# precip_mean_new.to_csv('precip_anom_std_new.csv',index=False)
# precip_mean_old.to_csv('precip_anom_std_old.csv',index=False)

