import os
import xarray as xr
import pandas as pd     
import numpy as np
import math
import datetime
from dateutil.relativedelta import relativedelta

os.chdir('')
origine_prate = xr.open_dataset('prate.sfc.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')  
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc') 

# Unit : Kg/m^2/s -> mm/month
for i in range(len(prate.time)):
    p_time = str(prate.time[i].values)[:10]
    b = datetime.datetime.strptime(p_time, '%Y-%m-%d')
    nums_of_day = ((b + relativedelta(months=i)) - datetime.timedelta(days=1)).day
    sec_to_month = 60*60*24*nums_of_day
    new_ds=origine_prate.prate * sec_to_month

prate= new_ds
land = mask_file.land
landsea = asia_mask_file.LANDSEA

prate_sel = new_ds.sel(lon=slice(110,150), lat = slice(53.5,20))
prate_sel

asia_lon = asia_mask_file.XA # lon
asia_lat = asia_mask_file.YA # lat

sel_new_grid = prate_sel.interp(lon = asia_lon, lat = asia_lat)
sel_new_grid

sel_new_grid['landsea'] = landsea
prate['land'] = land

weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glob = np.cos(np.deg2rad(prate[0].lat))


length_prate= len(sel_new_grid)

yellow_sea_lst = []
east_china_sea = []
east_sea = []
east_asia_sea = []
glob_lst = []

time_lst = []

for i in range(length_prate):
    p_time = str(sel_new_grid.time[i].values)[:10]
    
    yel_weight = sel_new_grid[i].where(sel_new_grid.landsea==1).weighted(weight_asia)
    result = yel_weight.mean(('XA', 'YA')).values
    yellow_sea_lst.append(result)
    
    
    echina_weight = sel_new_grid[i].where(sel_new_grid.landsea==2).weighted(weight_asia)
    result2 = echina_weight.mean(('XA', 'YA')).values
    east_china_sea.append(result2)
    
    esea_weight = sel_new_grid[i].where(sel_new_grid.landsea==3).weighted(weight_asia)
    result3 = esea_weight.mean(('XA', 'YA')).values
    east_sea.append(result3)


    easiasea_weight = sel_new_grid[i].where(sel_new_grid.landsea!=0).weighted(weight_asia)
    result4 = easiasea_weight.mean(('XA', 'YA')).values
    east_asia_sea.append(result3)
    
    
    glob_weight = prate[i].where(prate[0].land==0).weighted(weight_glob)
    result5 = glob_weight.mean(('lon','lat')).values
    glob_lst.append(result5)
    
    
    time_lst.append(p_time)

new_df = pd.DataFrame({'date':time_lst,'global':glob_lst,'east_sea':east_sea,'yellow_sea':yellow_sea_lst,
                       'east_china':east_china_sea,'east_asia':east_asia_sea})
new_df.reset_index(drop=True, inplace=True)

new_order = ['date','glb_mean', 'ask_mean', 'es_mean', 'ys_mean', 'ecs_mean']
new_df = new_df[new_order]
new_df.rename(columns={'data':'data','global':'glb_mean','east_asia':'ask_mean','east_sea':'es_mean','yellow_sea':'ys_mean','east_china':'ecs_mean'},inplace=True)
new_df

os.getcwd()
new_df.to_csv('prate_asia_mask&weighted2.csv',index=False)

