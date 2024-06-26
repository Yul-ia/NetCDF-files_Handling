import numpy as np
import pandas as pd
import xarray as xr
import os
import datetime
from dateutil.relativedelta import relativedelta

#%%
os.getcwd()
os.chdir('')

ds_u = xr.open_dataset('uwnd.10m.mon.mean.nc')
ds_v = xr.open_dataset('vwnd.10m.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')

## wind
uv_wnd = np.sqrt((ds_u.uwnd)**2+(ds_v.vwnd)**2)

# masking
landsea =mask_file.land
uv_wnd['land'] = landsea

length_wind = len(uv_wnd)

lst = []
time_lst = []

weight = np.cos(np.deg2rad(uv_wnd.lat)) # weighting
for i in range(length_wind):
    uv_wnd_weighted = uv_wnd[i].where(uv_wnd[0].land==0).weighted(weight) # apply weighting to the wind
    result = uv_wnd_weighted.mean(('lon','lat')).values[0] # weighted average
    
    new_time = str(uv_wnd[i].time.values)[:10]
    
    lst.append(result)
    time_lst.append(new_time)
    
new_df = pd.DataFrame({'time':time_lst,'uv_wnd[m/s]':lst})
new_df

new_df.to_csv('uv_wnd_weighted.csv',index=False)
