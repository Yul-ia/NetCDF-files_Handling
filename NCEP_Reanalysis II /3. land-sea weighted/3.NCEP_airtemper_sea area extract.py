import os
import xarray as xr
import numpy as np
import glob
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

os.getcwd()
os.chdir('')

air_temp = xr.open_dataset('air.2m.mon.mean.nc') 
mask_file = xr.open_dataset('landsea.nc')  

air = air_temp.air
    
land = mask_file.land 
air['land'] =land 

air1=air[0]
len(air.values)
air1.where(air1.land==0).plot() 


air[1].where(air[0].land==0).mean()-273.15 
lenght_air = len(air)

lst = []
time_for_df =[]
weight = np.cos(np.deg2rad(air[0].lat))

for i in range(lenght_air):

    air_weight = air[i].where(air[0].land==0).weighted(weight) 
    result = (air_weight.mean(('lon','lat'))-273.15).values[0]
    air_time = str(air[i].time.values)[:10]
    
    lst.append(result)
    time_for_df.append(air_time) 

 
new_df = pd.DataFrame({'time':time_for_df,'air_weight':lst})
new_df.to_csv('air_temper_weight.csv',index=False)
