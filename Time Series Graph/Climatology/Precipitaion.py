import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.image as image
from matplotlib.offsetbox import(OffsetImage,AnnotationBbox)

#%%
def group_plot(era5_new, cmap_new, ncep_r2_new,
               clim_col_name ='glb_clim', std_col_name = 'glb_std',
               y_range = (80, 125, 5),
               title = 'Precipitaion Climatology',
               dir = '', file_name = 'clim', title_suffix = '1991-2020',
               y_label = 'Precipitation Rate[mm]'):
    plt.figure(figsize=(15, 6))
    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False

    mon = era5_new['month'].value_counts().index
    
    era5_clim_var = era5_new[clim_col_name].values[:12]
    cmap_clim_var = cmap_new[clim_col_name].values[:12]
    ncep_clim_var = ncep_r2_new[clim_col_name].values[:12]
    # Standard deviation plot
    era5_std_var = []
    for i in range(1, 13):
        std_var = era5_new.loc[era5_new['month'] == i][f'{std_col_name}_0.5'].values[0]
        era5_std_var.append(std_var*2)
        
    # cmap_std_var = cmap_new[std_col_name].value_counts().index
    # ncep_std_var = ncep_r2_new[std_col_name].value_counts().index
    cmap_std_var = cmap_new[std_col_name].values[:12]
    ncep_std_var = ncep_r2_new[std_col_name].values[:12]


    plt.plot(mon, era5_clim_var, marker='o', linestyle='-', color='#141567', markersize=4, label='ERA5')
    plt.fill_between(mon, era5_clim_var - era5_std_var, era5_clim_var + era5_std_var, color='#091A30', alpha=0.2,label='ERA5_std')
    
    plt.plot(mon, cmap_clim_var, marker='o', linestyle='-', color='#7877FF', markersize=4, label='CMAP')
    plt.fill_between(mon, cmap_clim_var - cmap_std_var, cmap_clim_var + cmap_std_var, color='#7877FF', alpha=0.2,label='CMAP_std')
    
    plt.plot(mon, ncep_clim_var, marker='o', linestyle='-', color='#00B7F0', markersize=4, label='NCEP_R2')
    plt.fill_between(mon, ncep_clim_var - ncep_std_var, ncep_clim_var + ncep_std_var, color='#00B7F0', alpha=0.2,label='NCEP_R2_std')


    plt.yticks(np.arange(*y_range),fontsize=12)
    tick_label = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    plt.xticks(ticks=mon, labels=tick_label, fontsize=12)

    plt.title(f'{title} ({title_suffix})', fontsize=16, weight='bold',y=1.04)
    plt.ylabel(y_label, weight='bold', fontsize=16, x=0.3)

    # Add legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=12, frameon=False)

    # Add grid
    plt.grid(axis='y')

    # Add logo
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.8, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)


    os.chdir(dir)
    img_file = f'{file_name}_{title_suffix}_{i}.png'
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    # plt.close()
    plt.show()



#%%
#################################################################################
def subplot_plot(era5_new, cmap_new, ncep_r2_new,
                      clim_col_name = 'glb_mean',std_col_name = 'glb_std',
                      y_range=(80, 125, 5),
                      title = 'Global Sea Climatology Precipitation',
                      dir='', file_name='MM', title_suffix='1994-2023',
                      y_label='Precipitation Rate[mm]'):


    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False
    
    mon = era5_new['month'].value_counts().index

    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharey=True)  #3행 1열
    
    era5_clim_var = era5_new[clim_col_name].values[:12]
    cmap_clim_var = cmap_new[clim_col_name].values[:12]
    ncep_clim_var = ncep_r2_new[clim_col_name].values[:12]

    
    era5_std_var = []
    for i in range(1, 13):
        e_std = era5_new.loc[era5_new['month'] == i][f'{std_col_name}_0.5'].values[0]

        era5_std_var.append(e_std*2)


    cmap_std_var = cmap_new[std_col_name].value_counts().index
    ncep_std_var = ncep_r2_new[std_col_name].value_counts().index


    axes[0].plot(mon, era5_clim_var, marker='o', linestyle='-', color='#141567', markersize=4, label='ERA5')
    axes[0].fill_between(mon, era5_clim_var - era5_std_var, era5_clim_var + era5_std_var, color='#091A30', alpha=0.2,label='ERA5_std')
    
    axes[1].plot(mon, cmap_clim_var, marker='o', linestyle='-', color='#7877FF', markersize=4, label='CMAP')
    axes[1].fill_between(mon, cmap_clim_var - cmap_std_var, cmap_clim_var + cmap_std_var, color='#7877FF', alpha=0.2,label='CMAP_std')
    
    axes[2].plot(mon, ncep_clim_var, marker='o', linestyle='-', color='#00B7F0', markersize=4, label='NCEP_R2')
    axes[2].fill_between(mon, ncep_clim_var - ncep_std_var, ncep_clim_var + ncep_std_var, color='#00B7F0', alpha=0.2,label='NCEP_R2_std')


    fig.supylabel(y_label, weight='bold', fontsize=16)
    fig.suptitle(f'{title} ({title_suffix})', fontsize=16, weight='bold',y=0.94)
    
    # Add legend
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=12, frameon=False)
    
    # x_label
    tick_values = np.arange(1, 13)
    tick_labels = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']

    for ax in axes:
        ax.set_xticks(tick_values)  
        ax.set_xticklabels(tick_labels) 
        ax.set_yticks(np.arange(*y_range))
        ax.grid(axis='y') 

    plt.subplots_adjust(left=0.08, right=0.9,bottom=0.01,hspace=0.3)
    # logo
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.84, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    os.chdir(dir)
    img_file = f'{file_name}_{title_suffix}_{i}.png'
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    # plt.close()
    plt.show()
    

#%%
cmap_new = pd.read_csv('data/CMAP/6.CMAP_anom_std_csv/cmap_precip_(clim,anom,std)_new.csv')
cmap_old = pd.read_csv('data/CMAP/6.CMAP_anom_std_csv/cmap_precip_(clim,anom,std)_old.csv')
cmap_present = pd.read_csv('data/CMAP/6.CMAP_anom_std_csv/cmap_precip_(clim,anom,std)_present.csv')

ncep_r2_new = pd.read_csv('6.anom_std_csv/prate_anom_std_new.csv')
ncep_r2_old = pd.read_csv('6.anom_std_csv/prate_anom_std_old.csv')
ncep_r2_present = pd.read_csv('data/NCEP_R2/6.anom_std_csv/ncep_prate_(clim,anom,std)_present.csv')

era5_new = pd.read_csv('/prate_month_new.csv')
era5_old = pd.read_csv('/prate_month_old.csv')
era5_present = pd.read_csv('/prate_month_present.csv')

logo_path = 'd:/logo/logo1.png'
logo = image.imread(logo_path)

#%%
era5_new['날짜'] = era5_new['날짜'].astype(str)
era5_new['year'] = era5_new['날짜'].str[:5]
era5_new['month'] = era5_new['날짜'].str[6:9]

era5_old['날짜'] = era5_old['날짜'].astype(str)
era5_old['year'] = era5_old['날짜'].str[:5]
era5_old['month'] = era5_old['날짜'].str[6:9]

era5_present['날짜'] = era5_present['날짜'].astype(str)
era5_present['year'] = era5_present['날짜'].str[:5]
era5_present['month'] = era5_present['날짜'].str[6:9]

era5_new['year'] = era5_new['year'].str.replace('\ufeff', '').astype(int)
era5_new['month'] = era5_new['month'].astype(int)

era5_old['year'] = era5_old['year'].str.replace('\ufeff', '').astype(int)
era5_old['month'] = era5_old['month'].astype(int)


era5_present['year'] = era5_present['year'].str.replace('\ufeff', '').astype(int)
era5_present['month'] = era5_present['month'].astype(int)

new_col = ['date',  'glb_mean', 'glb_clim', 'glb_anom','glb_std_0.5','ask_mean',
       'ask_clim', 'ask_anom', 'ask_std_0.5', 'es_mean', 'es_clim', 'es_anom',
       'es_std_0.5', 'ys_mean', 'ys_clim', 'ys_anom', 'ys_std_0.5', 'ecs_mean',
       'ecs_clim', 'ecs_anom', 'ecs_std_0.5','year','month']

era5_new.columns = new_col
era5_old.columns = new_col
era5_present.columns = new_col

cmap_new['date'] = pd.to_datetime(cmap_new['date'], format='%Y-%m-%d')
cmap_old['date'] = pd.to_datetime(cmap_old['date'], format='%Y-%m-%d')
cmap_present['date'] = pd.to_datetime(cmap_present['date'], format='%Y-%m-%d')

ncep_r2_new['date'] = pd.to_datetime(ncep_r2_new['date'], format='%Y-%m-%d')
ncep_r2_old['date'] = pd.to_datetime(ncep_r2_old['date'], format='%Y-%m-%d')
ncep_r2_present['date'] = pd.to_datetime(ncep_r2_present['date'], format='%Y-%m-%d')



    
#%%
########################################################################################################gbl_present
group_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_present', 
           file_name = "prate_glb_clim(3)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_present', 
           file_name = "prate_glb_clim(4)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')
#%%
########################################################################################################gbl_new
group_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_new', 
           file_name = "prate_glb_clim(3)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_new', 
           file_name = "prate_glb_clim(4)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################gbl_old
group_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_old', 
           file_name = "prate_glb_clim(3)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (70, 135, 10),
           title = 'Global Sea Climatology Precipitation',
           dir = 'climatology_present\prate\glb_old', 
           file_name = "prate_glb_clim(4)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')

# %%
########################################################################################################ask_present
group_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_present', 
           file_name = "prate_ask_clim(3)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_present', 
           file_name = "prate_ask_clim(4)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ask_new
group_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_new', 
           file_name = "prate_ask_clim(3)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_new', 
           file_name = "prate_ask_clim(4)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ask_old
group_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_old', 
           file_name = "prate_ask_clim(3)", 
           title_suffix = '1981-2010',cmap_clim_var = cmap_new[clim_col_name].values[:12]
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (30, 310, 30),
           title = 'East Asia Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ask_old', 
           file_name = "prate_ask_clim(4)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ys_present
group_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_present', 
           file_name = "prate_ys_clim(3)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_present', 
           file_name = "prate_ys_clim(4)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ys_new
group_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_new', 
           file_name = "prate_ys_clim(3)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_new', 
           file_name = "prate_ys_clim(4)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ys_old
group_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_old', 
           file_name = "prate_ys_clim(3)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (-10,291,40),
           title = 'Yellow Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ys_old', 
           file_name = "prate_ys_clim(4)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ecs_present
group_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_present', 
           file_name = "prate_ecs_clim(3)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_present', 
           file_name = "prate_ecs_clim(4)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ecs_new
group_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_new', 
           file_name = "prate_ecs_clim(3)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_new', 
           file_name = "prate_ecs_clim(4)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################ecs_old
group_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_old', 
           file_name = "prate_ecs_clim(3)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,361,40),
           title = 'East China Sea Climatology Precipitation',
           dir = '/climatology_present/prate/ecs_old', 
           file_name = "prate_ecs_clim(4)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################es_present
group_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_present', 
           file_name = "prate_es_clim(3)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_present, cmap_present, ncep_r2_present,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_present', 
           file_name = "prate_es_clim(4)", 
           title_suffix = '1994-2023',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################es_new
group_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_new', 
           file_name = "prate_es_clim(3)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_new, cmap_new, ncep_r2_new,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_new', 
           file_name = "prate_es_clim(4)", 
           title_suffix = '1991-2020',
           y_label = 'Precipitation Rate[mm]')
# %%
########################################################################################################es_old
group_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_old', 
           file_name = "prate_es_clim(3)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')

subplot_plot(era5_old, cmap_old, ncep_r2_old,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (20,201,20),
           title = 'East Sea Climatology Precipitation',
           dir = '/climatology_present/prate/es_old', 
           file_name = "prate_es_clim(4)", 
           title_suffix = '1981-2010',
           y_label = 'Precipitation Rate[mm]')
# %%
