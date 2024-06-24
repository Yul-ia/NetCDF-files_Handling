import os
import xarray as xr
import numpy as np
import pandas as pd
import glob
#%%
os.getcwd()
os.chdir('d:/NCEP_R2')
#%%
pres_origin = xr.open_dataset('pres.sfc.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')

pres = pres_origin.pres # 각 년도 각 월의 기압
landsea = mask_file.land

pres['land'] = landsea # pres array에 마스킹된 land 추가
length_pres = len(pres)

#%%
pres_weight_lst = []
time_for_df = []

for i in range(length_pres):
    weight = np.cos(np.deg2rad(pres[i]).lat)
    pres_weight = pres[i].where(pres[0].land==0).weighted(weight)
    result = pres_weight.mean(('lon','lat')).values
    
    pres_weight_lst.append(result)
    
    pres_time = pres[i].time.values
    time_for_df.append(pres_time)

new_df = pd.DataFrame({'time':time_for_df, 'pres_weight':pres_weight_lst})
#%%
### local에 저장
os.getcwd()
new_df.to_csv('pres_weight.csv')
