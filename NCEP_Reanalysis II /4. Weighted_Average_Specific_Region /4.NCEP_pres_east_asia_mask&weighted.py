import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

os.getcwd()
os.chdir('')

ds_pres = xr.open_dataset('pres.sfc.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc')

# Unit # Unit conversion: pa -> hpa
pa_to_hpa = 0.01 # [hPa]

pres = ds_pres.pres * pa_to_hpa
land = mask_file.land
landsea = asia_mask_file.LANDSEA

### grid 
pres_sel = ds_pres.sel(lon=slice(110,150), lat=slice(53.5,20))

asia_lon = asia_mask_file.XA # lon
asia_lat = asia_mask_file.YA # lat

sel_new_grid = pres_sel.interp(lon=asia_lon, lat= asia_lat) 

### mask
sel_new_grid['landsea']=landsea # east_asia_mask // dataset
pres['land'] = land # glob mask // data array


sel_new_grid_pres = sel_new_grid.pres*pa_to_hpa # Unit conversion: pa -> hpa

### weighted 
weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glob = np.cos(np.deg2rad(pres.lat))

### variable creation
length_pres = len(sel_new_grid.pres)

glb_lst = []
es_lst = [] # 3
ys_lst = [] # 1
ecs_lst=[] # 2
ask_lst =[] #!=0 

time_lst = []


for i in range(length_pres):
    ys_weight = sel_new_grid_pres[i].where(sel_new_grid.landsea == 1).weighted(weight_asia)
    result = ys_weight.mean(('XA','YA')).values
    ys_lst.append(result)
    
    ecs_weight = sel_new_grid_pres[i].where(sel_new_grid.landsea == 2).weighted(weight_asia)
    result2 =ecs_weight.mean(('XA','YA')).values
    ecs_lst.append(result2)
    
    es_weight = sel_new_grid_pres[i].where(sel_new_grid.landsea == 3).weighted(weight_asia)
    result3 = es_weight.mean(('XA','YA')).values
    es_lst.append(result3)
    
    ask_weight = sel_new_grid_pres[i].where(sel_new_grid.landsea !=0 ).weighted(weight_asia)
    result4 = ask_weight.mean(('XA','YA')).values
    ask_lst.append(result4)
    
    
    # glb_weight = pres_sel.pres[i].where(pres[0].land == 0).weighted(weight_glob)
    glb_weight = pres[i].where(pres[0].land==0).weighted(weight_glob) ### 위에랑 결과 다른지 비교
    result5 = glb_weight.mean(('lon','lat')).values
    glb_lst.append(result5)
    
    time_lst.append(str(sel_new_grid.time[i].values)[:10])
    


new_df = pd.DataFrame({'date':time_lst, 'glb_mean':glb_lst, 'ask_mean':ask_lst,
                       'es_mean':es_lst, 'ys_mean':ys_lst, 'ecs_mean': ecs_lst})
new_df.reset_index(drop=True, inplace=True)

new_df

os.getcwd()
new_df.to_csv('pres_asia_mask&weighted.csv',index=False)

    
    
    
    
