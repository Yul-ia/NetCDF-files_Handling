import xarray as xr
import numpy as np
import os
os.chdir('')

pres = xr.open_dataset("pres.sfc.mon.mean.nc")

pres_9120 = pres.sel(time=slice('1991-01-01','2020-12-01'))
pres_8110 = pres.sel(time=slice('1981-01-01','2010-12-01'))

### new clim
lon = pres_9120.lon
lat = pres_9120.lat
month = np.arange(1,13)

lst = []
for i in range(1,13):
    ds_new = pres_9120.sel(time=pres_9120['time.month']==i)
    pres_mean = ds_new.mean(dim='time')['pres']
    lst.append(pres_mean)

pres_arr = np.array(lst)

pres_9120_clim = xr.Dataset(
    data_vars=dict(
        pres = (['month','lat','lon'],pres_arr)
    ),
    coords= dict(
        lat = lat,
        lon = lon,
        month = month
    )
)

pres_9120_clim.pres.attrs = {'unit' : 'Pascals', 'long_name':'NCEP Long Term Mean Pressure at Surface'}
pres_9120_clim.lon.attrs = {'unit':'degrees_east', 'long_name' : "Longitude"}
pres_9120_clim.lat.attrs = {'unit': 'degrees_north', 'long_name': "Latitude"}

pres_9120_clim.to_netcdf("NECP_pres_clim_9120.nc")
