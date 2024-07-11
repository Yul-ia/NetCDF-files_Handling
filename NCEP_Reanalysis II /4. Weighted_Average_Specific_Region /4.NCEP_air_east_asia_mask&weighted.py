import os
import xarray as xr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from decimal import*
from decimal import Decimal, ROUND_HALF_UP
os.getcwd()
os.chdir('')

ds_air = xr.open_dataset('air.2m.mon.mean.nc')
mask_file = xr.open_dataset('landsea.nc')
asia_mask_file = xr.open_dataset('ASKmaskNew20230615.nc')

## asia def
def asia_weight_mean(idx,landsea_num):
    if landsea_num == 'not_0':
        condition = sel_new_grid.landsea !=0
    else:
        condition = sel_new_grid.landsea == landsea_num
        
    weight = air_eastasia[idx].where(condition).weighted(weight_asia)
    result = (weight.mean(('XA','YA'))).values
    return result
    
## global def
def glb_weight_mean(idx):
    weight = air[idx].where(air[0].land==0).weighted(weight_glb)
    result = (weight.mean(('lon','lat'))).values
    return result

# round_half_up def
def round_up (num):
    result =Decimal(num).quantize(Decimal('.00'),rounding = ROUND_HALF_UP)
    return result 


# ds_air = ds_air.drop_dims('level')
ds_air = ds_air.squeeze('level') 

air = ds_air.air-273.15  # before weight 단위 환산 먼저 하기
land = mask_file.land
lansea = asia_mask_file.LANDSEA

### grid
air_sel = ds_air.sel(lon=slice(110,150),lat=slice(53.5,20))

asia_lon = asia_mask_file.XA
asia_lat = asia_mask_file.YA

sel_new_grid =air_sel.interp(lon=asia_lon, lat=asia_lat)

### mask
sel_new_grid['landsea'] = lansea
air['land'] = land

air_eastasia = sel_new_grid.air - 273.15

weight_asia = np.cos(np.deg2rad(sel_new_grid.lat))
weight_glb = np.cos(np.deg2rad(air.lat))


length_air = len(sel_new_grid.air)

glb_lst=[]
es_lst =[]
ys_lst =[]
ecs_lst =[]
ask_lst =[]

time_lst =[]

for i in range(length_air):
    ys_lst.append(asia_weight_mean(i,1))
    ecs_lst.append(asia_weight_mean(i,2))
    es_lst.append(asia_weight_mean(i,3))
    ask_lst.append(asia_weight_mean(i,'not_0'))
    glb_lst.append(glb_weight_mean(i))
    
    time_lst.append(str(air[i].time.values)[:10])


    
new_df = pd.DataFrame({'date':time_lst, 'glb_mean':glb_lst, 'ask_mean':ask_lst,
                       'es_mean':es_lst, 'ys_mean':ys_lst, 'ecs_mean': ecs_lst})

new_df['date'] = pd.to_datetime(new_df['date'])
new_df['glb_mean'] = new_df['glb_mean'].astype(float)
new_df['ask_mean'] = new_df['ask_mean'].astype(float)
new_df['es_mean'] = new_df['es_mean'].astype(float)
new_df['ys_mean'] = new_df['ys_mean'].astype(float)
new_df['ecs_mean'] = new_df['ecs_mean'].astype(float)
new_df.info()

## option
# col_name = ['glb_mean', 'ask_mean', 'es_mean', 'ys_mean', 'ecs_mean']
# for col in col_name:
#     new_df[col] = new_df[col].apply(lambda x: float(round_up(Decimal(x)))) # round_up 함수 적용하기 위한 apply
# new_df.head()


new_df
os.getcwd()
new_df.to_csv('air_asia_mask&weighted.csv',index=False)



