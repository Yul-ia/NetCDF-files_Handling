import os
import numpy as np
import xarray as xr
import pandas as pd
import math
import datetime
from dateutil.relativedelta import relativedelta

os.getcwd()
os.chdir('')

prate_origin = xr.open_dataset('prate.sfc.mon.mean.nc')
mask_file =xr.open_dataset('landsea.nc')

prate = prate_origin.prate
landsea = mask_file.land

prate['land'] = landsea 
length_prate=len(prate)

lst = []
time_for_df =[]

weight = np.cos(np.deg2rad(prate[0].lat))

for i in range(length_prate):
    prate_weight = prate[i].where(prate[0].land==0).weighted(weight)
    result = prate_weight.mean(('lon','lat')).values
    
    p_time = str(prate[i].time.values)[:10]
    
    b=datetime.datetime.strptime(p_time, '%Y-%m-%d')
    c = ((b + relativedelta(months=i)) - datetime.timedelta(days=1)).day
    nums_of_day = c

    # Unit conversion : Kg/m^2/s -> mm/month
    sec_to_month = 60 * 60 * 24 * nums_of_day
    result_mm_per_month = result * sec_to_month # [mm]
    
    lst.append(result_mm_per_month)
    time_for_df.append(p_time) 
  
new_df = pd.DataFrame({'time':time_for_df,'prate_weight':lst})

new_df.to_csv('prate_weight.csv', index=False)
