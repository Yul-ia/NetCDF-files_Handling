import os
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import matplotlib.font_manager as fm
import datetime
from dateutil.relativedelta import relativedelta
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from netCDF4 import Dataset
from matplotlib import rc 
import matplotlib.image as image
from  matplotlib.offsetbox import(OffsetImage, AnnotationBbox)
import time

#%%
## file read 
os.chdir('d:/CMAP')
old_precip = xr.open_dataset('8. CMAP_clim_anom_ncfile/CMAP_old_clim_anom.nc') # ds_precip

logo_path = 'd:\logo\logo2.png'
logo = image.imread(logo_path)

#%%
lon = old_precip.lon # lon = old_precip.variables['lon'][:]
lat = old_precip.lat
precip = old_precip.precip

## grid
precip, lon1 = add_cyclic_point(precip, coord=lon)
lon, lat = np.meshgrid(lon1,lat)

## lat, lon min max
lat_min, lat_max, lon_min, lon_max = lat.min(), lat.max(), lon.min(), lon.max()

## glb_precip_range
precip_min = 0
precip_max = 400

## color noramilize
norm = matplotlib.colors.Normalize(vmin= precip_min, vmax = precip_max)

year = old_precip.precip['time'].dt.year
mon = old_precip.precip['time'].dt.month

#%%
os.chdir('d:/CMAP/9.CMAP_plot/glovbal_mean_plot_old')

#%%
# plot
length = len(old_precip.precip)

start = time.perf_counter()
for i in range(length):
    
    plt.rc('font', family='Malgun Gothic', weight = 'bold')	 # font
    plt.rcParams['axes.unicode_minus'] =False
    %matplotlib inline

    fig = plt.figure(figsize=(15,11.5)) # figsize

    cmap = cm.get_cmap('PuBuGn') # colormap

    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=205))
    cs = plt.contourf(lon,lat,precip[i], cmap = cmap, norm=norm ,levels = np.linspace(precip_min, precip_max, 100), 
                      extend='max', transform=ccrs.PlateCarree())

    ## map tick
    plt.xticks(np.arange(-125,185,80),['80°E','160°E', '120°W', '40°W'], fontsize=25) 
    plt.yticks(np.arange(-90,91,45),['90°S', '45°S', 'EQ', '45°N', '90°N'], fontsize=25)
    plt.tick_params(axis='x', direction='out', pad=8, labelsize=25, labelcolor='black', top=False)

    # colorbar 
    tick_term= np.arange(precip_min,precip_max+1,50) 

    cbar = plt.colorbar(cs, ticks=tick_term, shrink=0.95, pad=0.09,orientation='horizontal', aspect=50) 
    cbar.ax.tick_params(labelsize=25)

    ## coastlines
    ax.coastlines(resolution='50m') 
    ax.set_aspect('auto', adjustable=None)


    plt.title('전지구 강수량(CMAP, %s년 %s월, mm)' %(year[i].values, mon[i].values), fontsize=25, pad=15,  weight = 'bold')
    img_file = 'precip_global_%s%02d_CMAP.png'%(year[i].values, mon[i].values)

    ## logo
    imagebox = OffsetImage(logo, zoom = 0.1)

    ## logo location
    ab = AnnotationBbox(imagebox, (870, 139), frameon=False, xycoords='figure points')
    ax.add_artist(ab)
    fig.savefig(img_file, dpi=110, bbox_inches='tight')

    plt.close()

    # plt.show()
    
end = time.perf_counter()
print('Time taken : ',(end-start)/60,'m')
print('Done')
