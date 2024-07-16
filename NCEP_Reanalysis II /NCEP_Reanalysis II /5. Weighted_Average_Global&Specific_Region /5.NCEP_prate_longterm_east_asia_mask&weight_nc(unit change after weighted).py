import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

os.getcwd()
os.chdir('')

clim_prate = xr.open_dataset('longterm/NECP_prate_clim_9120.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc')

prate_clim = clim_prate.prate_clim
land = mask_file.land
landsea = asia_mask_file.LANDSEA


prate_sel = clim_prate.sel(lon=slice(110,150), lat=slice(53.5,20))

asia_lon = asia_mask_file.XA
asia_lat = asia_mask_file.YA

sel_new_grid = prate_sel.interp(lon=asia_lon, lat=asia_lat)

### mask
sel_new_grid['landsea'] = landsea # 동아시아
clim_prate['land'] = land # 전지구

### weighted
weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glb = np.cos(np.deg2rad(clim_prate.lat))

len_prate_clim = len(sel_new_grid.prate_clim)

glb_lst = []
es_lst = [] # 3
ys_lst = [] # 1
ecs_lst=[] # 2
ask_lst =[] #!=0 

month_lst = []

for i in range(len_prate_clim):
    # Unit : Kg/m^2/s -> mm/month
    p_time = str(sel_new_grid.month[i].values)[:10]
    
    b=datetime.datetime.strptime(p_time, '%m')
    c = ((b + relativedelta(months=i)) - datetime.timedelta(days=1)).day
    nums_of_day = c
    sec_to_month = 60*60*24*nums_of_day
    
    ys_weight = sel_new_grid.prate_clim[i].where(sel_new_grid.landsea==1).weighted(weight_asia)
    result = ys_weight.mean(('XA','YA')).values
    ys_lst.append(result*sec_to_month)
    
    ecs_weight = sel_new_grid.prate_clim[i].where(sel_new_grid.landsea == 2).weighted(weight_asia)
    result2 =ecs_weight.mean(('XA','YA')).values
    ecs_lst.append(result2*sec_to_month)
    
    es_weight = sel_new_grid.prate_clim[i].where(sel_new_grid.landsea == 3).weighted(weight_asia)
    result3 = es_weight.mean(('XA','YA')).values
    es_lst.append(result3*sec_to_month)
    
    ask_weight = sel_new_grid.prate_clim[i].where(sel_new_grid.landsea !=0 ).weighted(weight_asia)
    result4 = ask_weight.mean(('XA','YA')).values
    ask_lst.append(result4*sec_to_month)
    
    glb_weight = clim_prate.prate_clim[i].where(clim_prate.land==0).weighted(weight_glb) ### 위에랑 결과 다른지 비교
    result5 = glb_weight.mean(('lon','lat')).values[0]
    glb_lst.append(result5*sec_to_month)
    
    month_lst.append(sel_new_grid.month[i].values)

  
new_df = pd.DataFrame({'month':month_lst, 'glb_clim':glb_lst, 'ask_clim':ask_lst,
                       'es_clim':es_lst, 'ys_clim':ys_lst, 'ecs_clim': ecs_lst})  
    
new_df=new_df.round(2)
new_df
os.getcwd()
new_df.to_csv('prate_new_longterm_east_asia_mask&weight.csv',index=False)
