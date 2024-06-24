import os
import xarray as xr
import numpy as np
import glob
import pandas as pd

air_temp = xr.open_dataset('.nc') # 원본 air_temp 파일
mask_file = xr.open_dataset('landsea.nc')  # land 부분 mask 파일

