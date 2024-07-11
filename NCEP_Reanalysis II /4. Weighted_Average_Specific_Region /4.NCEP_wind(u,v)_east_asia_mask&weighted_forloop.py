import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta


os.getcwd()
os.chdir('')

ds_u = xr.open_dataset('uwnd.10m.mon.mean.nc')
ds_v = xr.open_dataset('vwnd.10m.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc')

ds_u = ds_u.squeeze('level')
ds_v = ds_v.squeeze('level')

## wind
uv_wnd = np.sqrt((ds_u.uwnd)**2+(ds_v.vwnd)**2) ##array
land = mask_file.land
landsea = asia_mask_file.LANDSEA

wnd_sel = uv_wnd.sel(lon=slice(110,150),lat=slice(53.5,20))

asia_lon = asia_mask_file.XA
asia_lat = asia_mask_file.YA

sel_new_grid =wnd_sel.interp(lon=asia_lon, lat=asia_lat)

### mask
sel_new_grid['landsea'] = landsea
uv_wnd['land'] = land

weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glb = np.cos(np.deg2rad(uv_wnd.lat))

length_wnd = len(sel_new_grid)

glb_lst=[]
es_lst =[]
ys_lst =[]
ecs_lst =[]
ask_lst =[]

time_lst =[]

for i in range(length_wnd):
    ys_weight = sel_new_grid[i].where(sel_new_grid.landsea==1).weighted(weight_asia)
    result = ys_weight.mean(('XA','YA')).values
    ys_lst.append(result)
    
    es_weight = sel_new_grid[i].where(sel_new_grid.landsea==3).weighted(weight_asia)
    result2 = es_weight.mean(('XA','YA')).values
    es_lst.append(result2)
    
    ecs_weight = sel_new_grid[i].where(sel_new_grid.landsea==2).weighted(weight_asia)
    result3 = ecs_weight.mean(('XA','YA')).values
    ecs_lst.append(result3)
    
    ask_weight = sel_new_grid[i].where(sel_new_grid.landsea!=0).weighted(weight_asia)
    result4 = ask_weight.mean(('XA','YA')).values
    ask_lst.append(result4)
    
    glb_weight = uv_wnd[i].where(uv_wnd[0].land==0).weighted(weight_glb)
    result5 = glb_weight.mean(('lon','lat')).values
    glb_lst.append(result5)
    
    time_lst.append(str(uv_wnd[i].time.values)[:10])
    
new_df = pd.DataFrame({'date':time_lst, 'glb_mean':glb_lst, 'ask_mean':ask_lst,
                       'es_mean':es_lst, 'ys_mean':ys_lst, 'ecs_mean': ecs_lst})

new_df['glb_mean'] = new_df['glb_mean'].astype(float)
new_df['ask_mean'] = new_df['ask_mean'].astype(float)
new_df['es_mean'] = new_df['es_mean'].astype(float)
new_df['ys_mean'] = new_df['ys_mean'].astype(float)
new_df['ecs_mean'] = new_df['ecs_mean'].astype(float)

os.getcwd()
new_df.to_csv('wind_asia_mask&weighted.csv',index=False)
