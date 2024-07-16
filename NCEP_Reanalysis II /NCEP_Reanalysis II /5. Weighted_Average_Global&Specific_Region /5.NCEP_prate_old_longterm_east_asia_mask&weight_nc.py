import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

os.getcwd()
os.chdir('')

clim_prate = xr.open_dataset('longterm/NECP_prate_clim_8110.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc')

# Unit : Kg/m^2/s -> mm/month
unit = []
for i in range(12):
    p_time  =str(clim_prate.month[i].values)
    b = datetime.datetime.strptime(p_time, '%m') # month
    c = ((b+ relativedelta(months=i))-datetime.timedelta(days=1)).day 
    num_of_day = c 
    sec_to_month = 60*60*24*num_of_day
    unit.append(sec_to_month)

# Unit 
for i in range(12):
    clim_prate.prate_clim2.values[i] *= unit[i]
    
prate_clim = clim_prate.prate_clim2
land = mask_file.land
landsea = asia_mask_file.LANDSEA


prate_sel = prate_clim.sel(lon=slice(110,150), lat=slice(53.5,20))
asia_lon = asia_mask_file.XA
asia_lat = asia_mask_file.YA

sel_new_grid = prate_sel.interp(lon=asia_lon, lat=asia_lat)

### mask
sel_new_grid['landsea'] = landsea 
land = land.squeeze('time')
prate_clim['land'] = land 

### weighted
weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glb = np.cos(np.deg2rad(prate_clim.lat))

len_prate_clim = len(sel_new_grid)

glb_lst = []
es_lst = [] # 3
ys_lst = [] # 1
ecs_lst=[] # 2
ask_lst =[] #!=0

month_lst = []

for i in range(len_prate_clim):
    ys_weight = sel_new_grid[i].where(sel_new_grid.landsea==1).weighted(weight_asia)
    result = ys_weight.mean(('XA','YA')).values
    ys_lst.append(result)
    
    ecs_weight = sel_new_grid[i].where(sel_new_grid.landsea == 2).weighted(weight_asia)
    result2 =ecs_weight.mean(('XA','YA')).values
    ecs_lst.append(result2)
    
    es_weight = sel_new_grid[i].where(sel_new_grid.landsea == 3).weighted(weight_asia)
    result3 = es_weight.mean(('XA','YA')).values
    es_lst.append(result3)
    
    ask_weight = sel_new_grid[i].where(sel_new_grid.landsea !=0 ).weighted(weight_asia)
    result4 = ask_weight.mean(('XA','YA')).values
    ask_lst.append(result4)
    
    glb_weight = prate_clim[i].where(prate_clim.land==0).weighted(weight_glb) ### 위에랑 결과 다른지 비교
    result5 = glb_weight.mean(('lon','lat')).values
    glb_lst.append(result5)
    
    month_lst.append(sel_new_grid.month[i].values)

  
new_df = pd.DataFrame({'month':month_lst, 'glb_clim':glb_lst, 'ask_clim':ask_lst,
                       'es_clim':es_lst, 'ys_clim':ys_lst, 'ecs_clim': ecs_lst})  
    

new_df
os.getcwd()
new_df.to_csv('prate_old_longterm_east_asia_mask&weight.csv',index=False)
