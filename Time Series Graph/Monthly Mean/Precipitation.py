import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib.image as image
import datetime as dt
from matplotlib.offsetbox import(OffsetImage,AnnotationBbox)

os.chdir('')

cmap_new = pd.read_csv('')
cmap_old = pd.read_csv('')
ncep_r2_new = pd.read_csv('')
ncep_r2_old = pd.read_csv('')
era5_new = pd.read_csv('')
era5_old = pd.read_csv('')

logo_path = 'd:/logo/logo1.png'
logo = image.imread(logo_path)


#%%
era5_new['날짜'] = era5_new['날짜'].astype(str)
era5_new['year'] = era5_new['날짜'].str[:5]
era5_new['month'] = era5_new['날짜'].str[6:9]

era5_old['날짜'] = era5_old['날짜'].astype(str)
era5_old['year'] = era5_old['날짜'].str[:5]
era5_old['month'] = era5_old['날짜'].str[6:9]


era5_new['year'] = era5_new['year'].str.replace('\ufeff', '').astype(int)
era5_new['month'] = era5_new['month'].astype(int)

era5_old['year'] = era5_old['year'].str.replace('\ufeff', '').astype(int)
era5_old['month'] = era5_old['month'].astype(int)
#%%
new_col = ['date',  'glb_mean', 'glb_clim', 'glb_anom','glb_std_0.5','ask_mean',
       'ask_clim', 'ask_anom', 'ask_std_0.5', 'es_mean', 'es_clim', 'es_anom',
       'es_std_0.5', 'ys_mean', 'ys_clim', 'ys_anom', 'ys_std_0.5', 'ecs_mean',
       'ecs_clim', 'ecs_anom', 'ecs_std_0.5','year','month']

era5_new.columns = new_col
era5_old.columns = new_col


cmap_new['date'] = pd.to_datetime(cmap_new['date'], format='%Y-%m-%d')
cmap_old['date'] = pd.to_datetime(cmap_old['date'], format='%Y-%m-%d')
ncep_r2_new['date'] = pd.to_datetime(ncep_r2_new['date'], format='%Y-%m-%d')
ncep_r2_old['date'] = pd.to_datetime(ncep_r2_old['date'], format='%Y-%m-%d')
#%%
########################################################################################################golbal_new
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_new_mon = era5_new.loc[era5_new['month'] == i]
    cmap_new_mon = cmap_new.loc[cmap_new['date'].dt.month==i]
    ncep_r2_new_mon = ncep_r2_new.loc[ncep_r2_new['date'].dt.month ==i]
    
    plt.plot(era5_new_mon['year'], era5_new_mon['glb_mean'], marker='o', linestyle='-', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_new_mon['date'].dt.year, cmap_new_mon['glb_mean'], marker='o', linestyle='-', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_new_mon['date'].dt.year, ncep_r2_new_mon['glb_mean'], marker='o', linestyle='-', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_new.loc[(era5_new['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(70,150,10))
    
    plt.title('Global Monthly Mean Precipitation (%s, 1991-2020)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')

    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_global_mean_1991_2020_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()


# %%
########################################################################################################golbal_old
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_old_mon = era5_old.loc[era5_old['month'] == i]
    cmap_old_mon = cmap_old.loc[cmap_old['date'].dt.month==i]
    ncep_r2_old_mon = ncep_r2_old.loc[ncep_r2_old['date'].dt.month ==i]
    
    plt.plot(era5_old_mon['year'], era5_old_mon['glb_mean'], marker='D', linestyle='dotted', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_old_mon['date'].dt.year, cmap_old_mon['glb_mean'], marker='D', linestyle='dotted', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_old_mon['date'].dt.year, ncep_r2_old_mon['glb_mean'], marker='D', linestyle='dotted', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_old.loc[(era5_old['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(70,150,10))

    plt.title('Global Monthly Mean Precipitation (%s, 1981-2010)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')

    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)


    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_global_mean_1981_2010_%s).png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()


# %%
########################################################################################################ask_new
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_new_mon = era5_new.loc[era5_new['month'] == i]
    cmap_new_mon = cmap_new.loc[cmap_new['date'].dt.month==i]
    ncep_r2_new_mon = ncep_r2_new.loc[ncep_r2_new['date'].dt.month ==i]
    
    plt.plot(era5_new_mon['year'], era5_new_mon['ask_mean'], marker='o', linestyle='-', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_new_mon['date'].dt.year, cmap_new_mon['ask_mean'], marker='o', linestyle='-', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_new_mon['date'].dt.year, ncep_r2_new_mon['ask_mean'], marker='o', linestyle='-', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_new.loc[(era5_new['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(40,270,30))

    plt.title('East Asia Sea Monthly Mean Precipitation (%s, 1991-2020)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    # 로고 
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ask_mean_1991_2020_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()
# %%
########################################################################################################ask_old
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_old_mon = era5_old.loc[era5_old['month'] == i]
    cmap_old_mon = cmap_old.loc[cmap_old['date'].dt.month==i]
    ncep_r2_old_mon = ncep_r2_old.loc[ncep_r2_old['date'].dt.month ==i]
    
    plt.plot(era5_old_mon['year'], era5_old_mon['ask_mean'], marker='D', linestyle='dotted', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_old_mon['date'].dt.year, cmap_old_mon['ask_mean'], marker='D', linestyle='dotted', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_old_mon['date'].dt.year, ncep_r2_old_mon['ask_mean'], marker='D', linestyle='dotted', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_old.loc[(era5_old['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(40,270,30))

    plt.title('East Asia Sea Monthly Mean Precipitation (%s, 1981-2010)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')


    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ask_mean_1981-2010_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()



# %%
########################################################################################################ys_new
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_new_mon = era5_new.loc[era5_new['month'] == i]
    cmap_new_mon = cmap_new.loc[cmap_new['date'].dt.month==i]
    ncep_r2_new_mon = ncep_r2_new.loc[ncep_r2_new['date'].dt.month ==i]
    
    plt.plot(era5_new_mon['year'], era5_new_mon['ys_mean'], marker='o', linestyle='-', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_new_mon['date'].dt.year, cmap_new_mon['ys_mean'], marker='o', linestyle='-', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_new_mon['date'].dt.year, ncep_r2_new_mon['ys_mean'], marker='o', linestyle='-', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_new.loc[(era5_new['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,340,30))

    plt.title('Yellow Sea Monthly Mean Precipitation (%s, 1991-2020)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ys_mean_1991_2020_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()

# %%
# %%
########################################################################################################ys_old
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_old_mon = era5_old.loc[era5_old['month'] == i]
    cmap_old_mon = cmap_old.loc[cmap_old['date'].dt.month==i]
    ncep_r2_old_mon = ncep_r2_old.loc[ncep_r2_old['date'].dt.month ==i]
    
    plt.plot(era5_old_mon['year'], era5_old_mon['ys_mean'], marker='D', linestyle='dotted', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_old_mon['date'].dt.year, cmap_old_mon['ys_mean'], marker='D', linestyle='dotted', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_old_mon['date'].dt.year, ncep_r2_old_mon['ys_mean'], marker='D', linestyle='dotted', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_old.loc[(era5_old['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,340,30))

    plt.title('Yellow Sea Monthly Mean Precipitation (%s, 1981-2010)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ys_mean_1981_2010_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()
# %%
########################################################################################################ecs_new
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_new_mon = era5_new.loc[era5_new['month'] == i]
    cmap_new_mon = cmap_new.loc[cmap_new['date'].dt.month==i]
    ncep_r2_new_mon = ncep_r2_new.loc[ncep_r2_new['date'].dt.month ==i]
    
    plt.plot(era5_new_mon['year'], era5_new_mon['ecs_mean'], marker='o', linestyle='-', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_new_mon['date'].dt.year, cmap_new_mon['ecs_mean'], marker='o', linestyle='-', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_new_mon['date'].dt.year, ncep_r2_new_mon['ecs_mean'], marker='o', linestyle='-', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_new.loc[(era5_new['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,510,50))

    plt.title('East China Sea Monthly Mean Precipitation (%s, 1991-2020)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ecs_mean_1991_2020_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()
# %%
########################################################################################################ecs_old
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_old_mon = era5_old.loc[era5_old['month'] == i]
    cmap_old_mon = cmap_old.loc[cmap_old['date'].dt.month==i]
    ncep_r2_old_mon = ncep_r2_old.loc[ncep_r2_old['date'].dt.month ==i]
    
    plt.plot(era5_old_mon['year'], era5_old_mon['ecs_mean'], marker='D', linestyle='dotted', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_old_mon['date'].dt.year, cmap_old_mon['ecs_mean'], marker='D', linestyle='dotted', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_old_mon['date'].dt.year, ncep_r2_old_mon['ecs_mean'], marker='D', linestyle='dotted', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_old.loc[(era5_old['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,510,50))

    plt.title('East China Sea Monthly Mean Precipitation (%s, 1981-2010)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_ecs_mean_1981_2010_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()
# %%
########################################################################################################es_new
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_new_mon = era5_new.loc[era5_new['month'] == i]
    cmap_new_mon = cmap_new.loc[cmap_new['date'].dt.month==i]
    ncep_r2_new_mon = ncep_r2_new.loc[ncep_r2_new['date'].dt.month ==i]
    
    plt.plot(era5_new_mon['year'], era5_new_mon['es_mean'], marker='o', linestyle='-', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_new_mon['date'].dt.year, cmap_new_mon['es_mean'], marker='o', linestyle='-', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_new_mon['date'].dt.year, ncep_r2_new_mon['es_mean'], marker='o', linestyle='-', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_new.loc[(era5_new['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,280,30))

    plt.title('East Sea Monthly Mean Precipitation (%s, 1991-2020)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_es_mean_1991_2020_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
    # plt.show()
# %%
########################################################################################################es_old
plt.rc('font', family = 'Malgun Gothic', weight = 'bold')
plt.rcParams['axes.unicode_minus'] = False
month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(1,13):
    plt.figure(figsize=(15,6))
    
    era5_old_mon = era5_old.loc[era5_old['month'] == i]
    cmap_old_mon = cmap_old.loc[cmap_old['date'].dt.month==i]
    ncep_r2_old_mon = ncep_r2_old.loc[ncep_r2_old['date'].dt.month ==i]
    
    plt.plot(era5_old_mon['year'], era5_old_mon['es_mean'], marker='D', linestyle='dotted', color='#141567', markersize= 4, label='ERA5')
    plt.plot(cmap_old_mon['date'].dt.year, cmap_old_mon['es_mean'], marker='D', linestyle='dotted', color='#8B8583', markersize = 4, label='CMAP')
    plt.plot(ncep_r2_old_mon['date'].dt.year, ncep_r2_old_mon['es_mean'], marker='D', linestyle='dotted', color='#61C7E5', markersize = 4, label='NCEP_R2')
    
    ticks = era5_old.loc[(era5_old['month']==1)]['year'].values # 30개 
    reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
    plt.xticks(ticks=reduced_ticks,fontsize=11)
    plt.yticks(np.arange(0,280,30))

    plt.title('East Sea Monthly Mean Precipitation (%s, 1981-2010)' %(month_label[i-1]), fontsize=15, weight='bold')
    plt.ylabel('Precipitation Rate[mm]', weight='bold',fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3,fontsize=12, frameon=False)
    plt.grid(axis='y')
    
    
    imagebox = OffsetImage(logo, zoom=0.07)
    ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
    plt.gca().add_artist(ab)

    plt.subplots_adjust(top=0.85, bottom=0.2)

    ## dir
    os.chdir('')
    img_file = 'prate_es_mean_1981_2010_%s.png' %(i)
    
    plt.savefig(img_file, dpi=110, bbox_inches='tight')
    plt.close()
# %%
