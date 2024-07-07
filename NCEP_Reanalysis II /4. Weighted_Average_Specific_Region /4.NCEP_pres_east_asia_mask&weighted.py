import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

os.chdir('')

ds_pres = xr.open_dataset('pres.sfc.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('')

pres = ds_pres.pres
land = mask_file.land
landsea = asia_mask_file.land

### grid 
pres_sel = ds_pres.sel(lon=slice(), lat=slice())

asia_lon = asia_mask_file.XA # lon
asia_lat = asia_mask_file.YA # lat

sel_new_grid = pres_sel.interp(lon=asia_lon, lat= asia_lat) # Grid adjustment

### mask
sel_new_grid['landsea']=landsea # east_asia_mask // dataset
pres['land'] = land # glob mask // data array

### weighted 
weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glob = np.cos(np.deg2rad(pres.lat))

### variable creation
length_pres = len(sel_new_grid.pres)

glb_lst = []
es_lst = [] 
ys_lst = [] 
ecs_lst=[] 
ask_lst =[] 

time_lst = []

# Unit # Unit conversion: pa -> hpa
pa_to_hpa = 0.01 # [hPa]

for i in range(length_pres):
    ys_weight = sel_new_grid.pres[i].where(sel_new_grid.landsea == '').weighted(weight_asia)
    result = ys_weight.mean(('lon','lat')).values
    ys_lst.append(result*pa_to_hpa)
    
    ecs_weight = sel_new_grid.pres[i].where(sel_new_grid.landsea == '').weighted(weight_asia)
    result2 =ecs_weight.mean(('lon','lat')).values
    ecs_lst.append(result2*pa_to_hpa)
    
    es_weight = sel_new_grid.pres[i].where(sel_new_grid.landsea == '').weighted(weight_asia)
    result3 = es_weight.mean(('lon','lat')).values
    es_lst.append(result3*pa_to_hpa)
    
    ask_weight = sel_new_grid.pres[i].where(sel_new_grid.landsea == '').weighted(weight_asia)
    result4 = ask_weight.mean(('lon','lat')).values
    ask_lst.append(result4*pa_to_hpa)
    
    glb_weight = pres[i].where(pres[0].land==0).weighted(weight_glob)
    result5 = glb_weight.mean(('lon','lat')).values
    glb_lst.append(result5*pa_to_hpa)
    
    time_lst.append(str(sel_new_grid.time[i].values)[:10])
    
new_df = pd.DataFrame({'date':time_lst, 'glb_mean':glb_lst, 'ask_mean':ask_lst,
                       'es_mean':es_lst, 'ys_mean':ys_lst, 'ecs_mean': ecs_lst})
new_df=new_df.round(2)
new_df

os.getcwd()
# new_df.to_csv('pres_asia_mask&weighted.csv',index=False)

     
