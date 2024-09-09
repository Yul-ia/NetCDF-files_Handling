import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.image as image
from matplotlib.offsetbox import(OffsetImage,AnnotationBbox)

#%%
def group_plot(era5_new, ncep_r2_new,
               clim_col_name ='glb_clim', std_col_name = '',
               y_range = (80, 125, 5),
               title = 'Surface Wind 10m',
               dir = '', file_name = 'clim', title_suffix = '1991-2020',
               y_label = 'Surface Wind 10m[m/s]'):
    plt.figure(figsize=(15, 6))
    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False

    mon = era5_new['month'].values[:12]
    
    era5_clim_var = era5_new[clim_col_name].values[:12]
    ncep_clim_var = ncep_r2_new[clim_col_name].values[:12]

    # STD
    era5_std_var = []
    for i in range(1, 13):
        std_var = era5_new.loc[era5_new['month'] == i][f'{std_col_name}_0.5'].values[0]
        era5_std_var.append(std_var*2)
        
    ncep_std_var = ncep_r2_new[std_col_name].values[:12]


    plt.plot(mon, era5_clim_var, marker='o', linestyle='-', color='#141567', markersize=4, label='ERA5')
    plt.fill_between(mon, era5_clim_var - era5_std_var, era5_clim_var + era5_std_var, color='#091A30', alpha=0.2,label='ERA5_std')
    

    plt.plot(mon, ncep_clim_var, marker='o', linestyle='-', color='#00B7F0', markersize=4, label='NCEP_R2')
    plt.fill_between(mon, ncep_clim_var - ncep_std_var, ncep_clim_var + ncep_std_var, color='#00B7F0', alpha=0.2,label='NCEP_R2_std')


    plt.yticks(np.arange(*y_range),fontsize=12)
    tick_label = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    plt.xticks(ticks=mon, labels=tick_label, fontsize=12)

    plt.title(f'{title} ({title_suffix})', fontsize=16, weight='bold',y=1.04)
    plt.ylabel(y_label, weight='bold', fontsize=16, x=0.3)

    # Add legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=12, frameon=False)

    # Add grid
    plt.grid(axis='y')

    # Add logo
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.8, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    # 파일 저장
    os.chdir(dir)
    img_file = f'{file_name}_{title_suffix}_{i}.png'
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    # plt.close()
    plt.show()



#%%
#################################################################################
def subplot_plot(era5_new, ncep_r2_new,
                      clim_col_name = 'glb_mean',std_col_name = 'glb_std',
                      y_range=(80, 125, 5),
                      title = 'Global Sea Climatology Surface Wind 10m',
                      dir='', file_name='MM', title_suffix='1994-2023',
                      y_label='Surface Wind 10m[m/s]'):


    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False
    
    mon = era5_new['month'].value_counts().index

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharey=True)  #3행 1열
    
    era5_clim_var = era5_new[clim_col_name].values[:12]
    ncep_clim_var = ncep_r2_new[clim_col_name].values[:12]

    era5_std_var = []
    for i in range(1, 13):
        e_std = era5_new.loc[era5_new['month'] == i][f'{std_col_name}_0.5'].values[0]

        era5_std_var.append(e_std*2)
        
    ncep_std_var = ncep_r2_new[std_col_name].values[:12]


    axes[0].plot(mon, era5_clim_var, marker='o', linestyle='-', color='#141567', markersize=4, label='ERA5')
    axes[0].fill_between(mon, era5_clim_var - era5_std_var, era5_clim_var + era5_std_var, color='#091A30', alpha=0.2,label='ERA5_std')
    
    axes[1].plot(mon, ncep_clim_var, marker='o', linestyle='-', color='#00B7F0', markersize=4, label='NCEP_R2')
    axes[1].fill_between(mon, ncep_clim_var - ncep_std_var, ncep_clim_var + ncep_std_var, color='#00B7F0', alpha=0.2,label='NCEP_R2_std')


    fig.supylabel(y_label, weight='bold', fontsize=16,x =-0.02)
    fig.suptitle(f'{title} ({title_suffix})', fontsize=16, weight='bold',y=0.94)
    
    # Add legend
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize=12, frameon=False)
    
    # x_label
    tick_values = np.arange(1, 13)
    tick_labels = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'] 

    for ax in axes:
        ax.set_xticks(tick_values) 
        ax.set_xticklabels(tick_labels) 
        ax.set_yticks(np.arange(*y_range))
        ax.grid(axis='y') 

    plt.subplots_adjust(left=0.08, right=0.9,bottom=-0.03,hspace=0.2,wspace=0.05)
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
os.chdir('')
ncep_r2_new = pd.read_csv('data/NCEP_R2/6.anom_std_csv/wind_anom_std_new.csv')
ncep_r2_old = pd.read_csv('data/NCEP_R2/6.anom_std_csv/wind_anom_std_old.csv')
ncep_r2_present = pd.read_csv('data/NCEP_R2/6.anom_std_csv/ncep_wind_(clim,anom,std)_present.csv')

era5_new = pd.read_csv('data/ERA5/windspeed_month_new.csv')
era5_old = pd.read_csv('data/ERA5/windspeed_month_old.csv')
era5_present = pd.read_csv('data/ERA5/windspeed_month_present.csv')

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


ncep_r2_new['date'] = pd.to_datetime(ncep_r2_new['date'], format='%Y-%m-%d')
ncep_r2_old['date'] = pd.to_datetime(ncep_r2_old['date'], format='%Y-%m-%d')
ncep_r2_present['date'] = pd.to_datetime(ncep_r2_present['date'], format='%Y-%m-%d')


#%%
########################################################################################################gbl_present
group_plot(era5_present, ncep_r2_present,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_present', 
           file_name = "wind_glb_clim(1)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_present, ncep_r2_present,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_present', 
           file_name = "wind_glb_clim(2)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')
#%%
########################################################################################################gbl_new
group_plot(era5_new, ncep_r2_new,
           clim_col_name ='glb_clim', std_col_name ='glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_new', 
           file_name = "wind_glb_clim(1)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_new, ncep_r2_new,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_new', 
           file_name = "wind_glb_clim(2)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################gbl_old
group_plot(era5_old, ncep_r2_old,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_old', 
           file_name = "wind_glb_clim(1)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_old, ncep_r2_old,
           clim_col_name ='glb_clim', std_col_name = 'glb_std',
           y_range = (3,6.1,0.5),
           title = 'Global Sea Climatology Surface Wind 10m',
           dir = 'climatology_present\wind\glb_old', 
           file_name = "wind_glb_clim(2)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

# %%
########################################################################################################ask_present
group_plot(era5_present, ncep_r2_present,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_present', 
           file_name = "wind_ask_clim(1)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_present, ncep_r2_present,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_present', 
           file_name = "wind_ask_clim(2)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ask_new
group_plot(era5_new, ncep_r2_new,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_new', 
           file_name = "wind_ask_clim(1)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_new, ncep_r2_new,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_new', 
           file_name = "wind_ask_clim(2)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ask_old
group_plot(era5_old, ncep_r2_old,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_old', 
           file_name = "wind_ask_clim(1)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_old, ncep_r2_old,
           clim_col_name ='ask_clim', std_col_name = 'ask_std',
           y_range = (0,8,1),
           title = 'East Asia Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ask_old', 
           file_name = "wind_ask_clim(2)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ys_present
group_plot(era5_present, ncep_r2_present,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_present', 
           file_name = "wind_ys_clim(1)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_present, ncep_r2_present,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_present', 
           file_name = "wind_ys_clim(2)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ys_new
group_plot(era5_new, ncep_r2_new,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_new', 
           file_name = "wind_ys_clim(1)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_new, ncep_r2_new,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_new', 
           file_name = "wind_ys_clim(2)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ys_old
group_plot(era5_old, ncep_r2_old,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_old', 
           file_name = "wind_ys_clim(1)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_old, ncep_r2_old,
           clim_col_name ='ys_clim', std_col_name = 'ys_std',
           y_range = (0,8,1),
           title = 'Yellow Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ys_old', 
           file_name = "wind_ys_clim(2)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ecs_present
group_plot(era5_present, ncep_r2_present,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_present', 
           file_name = "wind_ecs_clim(1)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_present, ncep_r2_present,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_present', 
           file_name = "wind_ecs_clim(2)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ecs_new
group_plot(era5_new, ncep_r2_new,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_new', 
           file_name = "wind_ecs_clim(1)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_new, ncep_r2_new,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_new', 
           file_name = "wind_ecs_clim(2)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################ecs_old
group_plot(era5_old, ncep_r2_old,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_old', 
           file_name = "wind_ecs_clim(1)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_old, ncep_r2_old,
           clim_col_name ='ecs_clim', std_col_name = 'ecs_std',
           y_range = (0,12,2),
           title = 'East China Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/ecs_old', 
           file_name = "wind_ecs_clim(2)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################es_present
group_plot(era5_present, ncep_r2_present,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_present', 
           file_name = "wind_es_clim(1)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_present, ncep_r2_present,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_present', 
           file_name = "wind_es_clim(2)", 
           title_suffix = '1994-2023',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################es_new
group_plot(era5_new, ncep_r2_new,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_new', 
           file_name = "wind_es_clim(1)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_new, ncep_r2_new,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_new', 
           file_name = "wind_es_clim(2)", 
           title_suffix = '1991-2020',
           y_label = 'Surface Wind 10m[m/s]')
# %%
########################################################################################################es_old
group_plot(era5_old, ncep_r2_old,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_old', 
           file_name = "wind_es_clim(1)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')

subplot_plot(era5_old, ncep_r2_old,
           clim_col_name ='es_clim', std_col_name = 'es_std',
           y_range = (0,11,2),
           title = 'East Sea Climatology Surface Wind 10m',
           dir = 'd:/plot_yuri/climatology_present/wind/es_old', 
           file_name = "wind_es_clim(2)", 
           title_suffix = '1981-2010',
           y_label = 'Surface Wind 10m[m/s]')
# %%
