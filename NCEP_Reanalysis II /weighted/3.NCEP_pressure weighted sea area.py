import os
import xarray as xr
import numpy as np
import pandas as pd
import glob
#%%
os.getcwd()
os.chdir('')
#%%
pres_origin = xr.open_dataset('pres.sfc.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')

pres = pres_origin.pres # pressure for each year and each month
landsea = mask_file.land

pres['land'] = landsea # add masked land to the pres array
length_pres = len(pres)

#%%
pres_weight_lst = []
time_for_df = []

weight = np.cos(np.deg2rad(pres[0]).lat)

# Unit
pa_to_hpa = 0.01 # [hPa]

for i in range(length_pres):

    pres_weight = pres[i].where(pres[0].land==0).weighted(weight)
    result = pres_weight.mean(('lon','lat')).values
    
    pres_time=str(pres[i].time.values)[:10]
    
    # Unit conversion: pa -> hpa
    result_hpa = result * pa_to_hpa # [hPa]
    
    pres_weight_lst.append(result_hpa)
    time_for_df.append(pres_time)

new_df = pd.DataFrame({'time':time_for_df, 'pres_weight':pres_weight_lst})

os.getcwd()
new_df.to_csv('pres_weight.csv')
