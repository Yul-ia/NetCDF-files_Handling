import os
import xarray as xr
import pandas as pd     
import numpy as np
import math
import datetime
from dateutil.relativedelta import relativedelta

os.chdir('')
ds_precip = xr.open_dataset('precip.mon.mean.nc') # [mm/day] > [mm/month]
mask_file = xr.open_dataset('CPC_landsea.nc')  # glb mask for CMAP
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc') 

# Unit : mm/day -> mm/month
for i in range(len(ds_precip.precip)):
    p_time = str(ds_precip.time[i].values)[:10] # '1979-03-01'
    b = datetime.datetime.strptime(p_time,'%Y-%m-%d')
    nums_of_day = ((b + relativedelta(months=i))-datetime.timedelta(days=1)).day
    ds_precip.precip[i] *= nums_of_day


precip = ds_precip.precip

land = mask_file.landsea # cpc mask
landsea = asia_mask_file.LANDSEA

## for glb grid 
new_sel = precip.sel(lon=slice(0,357.5), lat = slice(90,-90))
glb_lon = mask_file.X # lon
glb_lat = mask_file.Y # lat
glb_new_grid = new_sel.interp(lon = glb_lon, lat = glb_lat)

## for asia grid
precip_sel = precip.sel(lon=slice(110,150), lat = slice(53.5,20))
asia_lon = asia_mask_file.XA # lon
asia_lat = asia_mask_file.YA # lat
asia_new_grid = precip_sel.interp(lon = asia_lon, lat = asia_lat)

### mask
asia_new_grid['landsea'] = landsea # asia mask
glb_new_grid['land'] = land # glb mask

### weighted
weight_asia = np.cos(np.deg2rad(asia_new_grid.lat)) 
weight_glob = np.cos(np.deg2rad(glb_new_grid.lat)) 



length_precip= len(asia_new_grid)
glb_lst = []
es_lst = [] # 3
ys_lst = [] # 1
ecs_lst=[] # 2
ask_lst =[] #!=0

time_lst = []


for i in range(length_precip):
    p_time = str(glb_new_grid.time[i].values)[:10]
    
    yel_weight = asia_new_grid[i].where(asia_new_grid.landsea==1).weighted(weight_asia)
    result = yel_weight.mean(('XA', 'YA')).values
    ys_lst.append(result)
    
    
    echina_weight = asia_new_grid[i].where(asia_new_grid.landsea==2).weighted(weight_asia)
    result2 = echina_weight.mean(('XA', 'YA')).values
    ecs_lst.append(result2)
    
    esea_weight = asia_new_grid[i].where(asia_new_grid.landsea==3).weighted(weight_asia)
    result3 = esea_weight.mean(('XA', 'YA')).values
    es_lst.append(result3)

    easiasea_weight = asia_new_grid[i].where(asia_new_grid.landsea!=0).weighted(weight_asia) 
    result4 = easiasea_weight.mean(('XA', 'YA')).values
    ask_lst.append(result4)
    
    
    glob_weight = glb_new_grid[i].where(glb_new_grid[0].land==0).weighted(weight_glob)
    result5 = glob_weight.mean(('X','Y')).values
    glb_lst.append(result5)
    
    
    time_lst.append(p_time)

new_df = pd.DataFrame({'date':time_lst,'glb_mean':glb_lst, 'es_mean':es_lst,'ys_mean':ys_lst,
                       'ecs_mean':ecs_lst,'ask_mean':ask_lst})

new_df.reset_index(drop=True, inplace=True)
new_df

os.getcwd()
new_df.to_csv('precip_asia_mask&weighted.csv',index=False)
