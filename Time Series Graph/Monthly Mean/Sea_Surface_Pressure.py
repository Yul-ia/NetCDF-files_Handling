import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import matplotlib.image as image
import datetime as dt
from matplotlib.offsetbox import(OffsetImage,AnnotationBbox)
from scipy.stats import linregress
import matplotlib as mpl

#%%
##################################################################################################################### group plot
def group_plot(era5_df, ncep_df,
                      col_name = 'glb_mean',
                      start_year = '1994',
                      end_year = '2023',  
                      y_range=(70, 150, 10),
                      title = 'East Asia Monthly Mean pres',
                      dir='',file_name='MM',  title_suffix='1991-2020',
                      y_label='Sea Level Pressure[hPa]'):
        
    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False
    month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for i in range(1, 13):
        plt.figure(figsize=(16, 8))
        
        era5_df_mon = era5_df.loc[era5_df['month'] == i]
        ncep_df_mon = ncep_df.loc[ncep_df['date'].dt.month == i]
        

        ############################ trend 30
        x = np.arange(30)
        y_era5 = era5_df_mon[col_name].values
        y_ncep = ncep_df_mon[col_name].values

        # ERA5 선형 회귀
        slope_era5, intercept_era5, _, p_value_era5, _ = linregress(x, y_era5)
        trend_line_era5 = slope_era5 * x + intercept_era5

        # NCEP_R2 선형 회귀
        slope_ncep, intercept_ncep, _, p_value_ncep, _ = linregress(x, y_ncep)
        trend_line_ncep = slope_ncep * x + intercept_ncep
        
        ############################ trend 10 (14-23)
        x_ten = np.arange(10)
        y_era5_ten = era5_df_mon[col_name].values[20:]
        y_ncep_ten = ncep_df_mon[col_name].values[20:]
        
        # ERA5 선형 회귀
        slope_era5_ten, intercept_era5_ten, _, p_value_era5_ten, _ = linregress(x_ten, y_era5_ten)
        trend_line_era5_ten = slope_era5_ten * x_ten + intercept_era5_ten
        
        
        # NCEP_R2 선형 회귀
        slope_ncep_ten, intercept_ncep_ten, _, p_value_ncep_ten, _ = linregress(x_ten, y_ncep_ten)
        trend_line_ncep_ten = slope_ncep_ten * x_ten + intercept_ncep_ten
        
        ### trend 30year dotted line
        p_values_text_era5 = f'{start_year}~ : [{slope_era5:.2f}mm/30yr({p_value_era5:.2f})] '
        p_value_text_ncep = f'{start_year}~ : [{slope_ncep:.2f}mm/30yr({p_value_ncep:.2f})] '
        
        ### trend 10year line-red
        p_values_text_era5_ten = f'{end_year}~ : [{slope_era5_ten:.2f}mm/10yr({p_value_era5_ten:.2f})]' ## [Trendmm/10yr (p-values)] 
        p_value_text_ncep_ten = f'{end_year}~ : [ {slope_ncep_ten:.2f}mm/10yr({p_value_ncep_ten:.2f})]'


        # trend 10year label-red 
        plt.annotate('ERA5', xy=(era5_df_mon['year'].values[-10], trend_line_era5_ten[-10]),
                     xytext=(-40, 6), textcoords='offset points', color='#EF685B', fontsize=10)
        plt.annotate('NCEP R2', xy=(ncep_df_mon['date'].dt.year.values[-10], trend_line_ncep_ten[-10]),
                     xytext=(-40, 0), textcoords='offset points', color='#EF685B', fontsize=10)


        plt.plot(era5_df_mon['year'], era5_df_mon[col_name], marker='o', linestyle='-', color='#1E209D', markersize=4, label='ERA5')
        plt.plot(era5_df_mon['year'].values, trend_line_era5, linestyle='dotted', color='#1E209D', alpha=0.8, label = p_values_text_era5)
        plt.plot(era5_df_mon['year'].values[20:], trend_line_era5_ten, color='#EF685B', alpha=0.8,  label= p_values_text_era5_ten)          
                        
        plt.plot(ncep_df_mon['date'].dt.year, ncep_df_mon[col_name], marker='o', linestyle='-', color='#00B7F0', markersize=4, label='NCEP_R2')
        plt.plot(era5_df_mon['year'].values, trend_line_ncep, linestyle='dotted', color='#018DEB', alpha=0.8, label = p_value_text_ncep)
        plt.plot(era5_df_mon['year'].values[20:], trend_line_ncep_ten, color='#EF685B', alpha=0.8, label = p_value_text_ncep_ten )


        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=12, frameon=False, columnspacing=6)
        #########
        ticks = era5_df.loc[(era5_df['month']==1)]['year'].values # 30개 
        reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))
        plt.xticks(ticks=reduced_ticks,fontsize=11)
        plt.yticks(np.arange(*y_range))
        
        plt.title(f'{title} ({month_label[i-1]}, {title_suffix})', fontsize=15, weight='bold')
        plt.ylabel(y_label, weight='bold', fontsize=12)
        
        plt.grid(axis='y')
        
        # logo
        imagebox = OffsetImage(logo, zoom=0.07)
        ab = AnnotationBbox(imagebox, (0.78, 0.05), frameon=False, xycoords='figure fraction')
        plt.gca().add_artist(ab)

        # 여백 조정 (top, bottom, left, right)
        plt.subplots_adjust(top=0.85, bottom=0.2)

        # 파일 저장
        os.chdir(dir)
        img_file = f'{file_name}_{title_suffix}_{i}.png'
        plt.savefig(img_file, dpi=110, bbox_inches='tight')
        plt.close()
        # plt.show()


#%%
##################################################################################################################### subplot
def subplot_plot(era5_df, ncep_df,
                      col_name = 'glb_mean',
                      start_year = '1994',
                      end_year = '2023', 
                      y_range=(70, 150, 10),
                      title = 'East Asia Monthly Mean pres',
                      dir='', file_name='MM', title_suffix='1991-2020',
                      y_label='Sea Level Pressure[hPa]'):
        
    plt.rc('font', family='Malgun Gothic', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False
    month_label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for i in range(1, 13):
        fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharey=True)  #3행 1열
        
        era5_df_mon = era5_df.loc[era5_df['month'] == i]
        ncep_df_mon = ncep_df.loc[ncep_df['date'].dt.month == i]
        
        
        ############################ trend 30
        x = np.arange(30)
        y_era5 = era5_df_mon[col_name].values
        y_ncep = ncep_df_mon[col_name].values

        # ERA5 선형 회귀
        slope_era5, intercept_era5, _, p_value_era5, _ = linregress(x, y_era5)
        trend_line_era5 = slope_era5 * x + intercept_era5

        # NCEP_R2 선형 회귀
        slope_ncep, intercept_ncep, _, p_value_ncep, _ = linregress(x, y_ncep)
        trend_line_ncep = slope_ncep * x + intercept_ncep
        
        ############################ trend 10 (14-23)
        x_ten = np.arange(10)
        y_era5_ten = era5_df_mon[col_name].values[20:]
        y_ncep_ten = ncep_df_mon[col_name].values[20:]
        
        # ERA5 선형 회귀
        slope_era5_ten, intercept_era5_ten, _, p_value_era5_ten, _ = linregress(x_ten, y_era5_ten)
        trend_line_era5_ten = slope_era5_ten * x_ten + intercept_era5_ten
        
        # NCEP_R2 선형 회귀
        slope_ncep_ten, intercept_ncep_ten, _, p_value_ncep_ten, _ = linregress(x_ten, y_ncep_ten)
        trend_line_ncep_ten = slope_ncep_ten * x_ten + intercept_ncep_ten
        

        #### monthly mean plot
        ## ERA5
        axes[0].plot(era5_df_mon['year'], era5_df_mon[col_name], marker='o', linestyle='-', color='#1E209D', markersize=4, label='ERA5')
        axes[0].set_title('ERA5', loc = 'right', fontsize = 11, weight='bold')
        
        ## NCEP_R2
        axes[1].plot(ncep_df_mon['date'].dt.year, ncep_df_mon[col_name], marker='o', linestyle='-', color='#018DEB', markersize=4, label='NCEP_R2')
        axes[1].set_title('NCEP_R2', loc = 'right', fontsize = 11, weight='bold')

        
        axes[0].plot(era5_df_mon['year'].values, trend_line_era5, linestyle='dotted', color='#1E209D', label =f'{start_year}~ : [{slope_era5:.2f}mm/30yr({p_value_era5:.2f})] ' )
        axes[1].plot(era5_df_mon['year'].values, trend_line_ncep, linestyle='dotted', color='#018DEB',label = f'{start_year}~ : [{slope_ncep:.2f}mm/30yr({p_value_ncep:.2f})] ')

        axes[0].plot(era5_df_mon['year'].values[20:], trend_line_era5_ten, color='#EF685B', alpha=0.8, label=f'{end_year}~ : [{slope_era5_ten:.2f}mm/10yr({p_value_era5_ten:.2f})]')
        axes[1].plot(era5_df_mon['year'].values[20:], trend_line_ncep_ten, color='#EF685B', alpha=0.8, label=f'{end_year}~ : [{slope_ncep_ten:.2f}mm/10yr({p_value_ncep_ten:.2f})]')
        
        fig.legend(loc='upper center', bbox_to_anchor=(0.45, -0.02), ncol=2, fontsize=11, frameon=False, columnspacing=4)
    
        ticks = era5_df.loc[(era5_df['month']==1)]['year'].values # 30개 
        reduced_ticks = np.concatenate(([ticks[0]], ticks[1:-1][::2], [ticks[-1]]))

        for ax in axes:
            ax.set_xticks(ticks=reduced_ticks)
            ax.set_yticks(np.arange(*y_range))
            ax.grid(axis='y')
        
        ## y-label
        fig.supylabel(y_label, weight='bold',fontsize=16)
        ## title
        fig.suptitle(f'{title} ({month_label[i-1]}, {title_suffix})', fontsize=16, weight='bold')

        ## 여백 
        plt.subplots_adjust(left=0.08, top=0.9, bottom=0.05, hspace=0.4)  # 서브플롯 간 간격 조정

        # 로고 추가
        imagebox = OffsetImage(logo, zoom=0.07)
        ab = AnnotationBbox(imagebox, (0.86, 0.03), frameon=False, xycoords='figure fraction')
        plt.gca().add_artist(ab)

        # 파일 저장 및 그래프 출력
        os.chdir(dir)
        img_file = f'{file_name}_{title_suffix}_{i}.png'
        plt.savefig(img_file, dpi=110, bbox_inches='tight')
        plt.close()
        # plt.show()


#%%
##################################################################################################################### pres
### monthly mean & trend
os.chdir('')

ncep_r2_new = pd.read_csv('data/NCEP_R2/6.anom_std_csv/pres_anom_std_new.csv')
ncep_r2_old = pd.read_csv('data/NCEP_R2/6.anom_std_csv/pres_anom_std_old.csv')
ncep_r2_present = pd.read_csv('data/NCEP_R2/6.anom_std_csv/ncep_pres_(clim,anom,std)_present.csv')

era5_new = pd.read_csv('data/ERA5/surfpres_month_new.csv')
era5_old = pd.read_csv('data/ERA5/surfpres_month_old.csv')
era5_present = pd.read_csv('data/ERA5/surfpres_month_present.csv')

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
                  col_name='glb_mean',
                  start_year='1994',
                  end_year='2023',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_present',
                  file_name = "pres_glb_mean(1)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_present, ncep_r2_present,
                  col_name='glb_mean',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_present',
                  file_name = "pres_glb_mean(2)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################gbl_new
group_plot(era5_new, ncep_r2_new,
                  col_name='glb_mean',
                  start_year='1991',
                  end_year='2020',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_new',
                  file_name = "pres_glb_mean(1)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_new, ncep_r2_new,
                  col_name='glb_mean',
                  start_year='1991',
                  end_year='2020',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_new',
                  file_name = "pres_glb_mean(2)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################gbl_old
group_plot(era5_old, ncep_r2_old,
                  col_name='glb_mean',
                  start_year='1981',
                  end_year='2010',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_old',
                  file_name = "pres_glb_mean(1)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_old, ncep_r2_old,
                  col_name='glb_mean',                  
                  start_year='1981',
                  end_year='2010',
                  y_range=(1007.5,1013,0.5),
                  title = 'Global Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/glb_old',
                  file_name = "pres_glb_mean(2)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ask_present
group_plot(era5_present, ncep_r2_present,
                  col_name='ask_mean',                  
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_present',
                  file_name = "pres_ask_mean(1)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_present, ncep_r2_present,
                  col_name='ask_mean',
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_present',
                  file_name = "pres_ask_mean(2)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ask_new
group_plot(era5_new, ncep_r2_new,
                  col_name='ask_mean',       
                  start_year='1991',
                  end_year='2020',
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_new',
                  file_name = "pres_ask_mean(1)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_new, ncep_r2_new,
                  col_name='ask_mean',
                  start_year='1991',
                  end_year='2020',
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_new',
                  file_name = "pres_ask_mean(2)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ask_old
group_plot(era5_old, ncep_r2_old,
                  col_name='ask_mean',
                  start_year='1981',
                  end_year='2010',
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_old',
                  file_name = "pres_ask_mean(1)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_old, ncep_r2_old,
                  col_name='ask_mean',
                  start_year='1981',
                  end_year='2010',
                  y_range=(995, 1031, 5),
                  title = 'East Asia Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ask_old',
                  file_name = "pres_ask_mean(2)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ys_present
group_plot(era5_present, ncep_r2_present,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_present',
                  file_name = "pres_ys_mean(1)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_present, ncep_r2_present,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_present',
                  file_name = "pres_ys_mean(2)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ys_new
group_plot(era5_new, ncep_r2_new,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_new',
                  file_name = "pres_ys_mean(1)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_new, ncep_r2_new,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_new',
                  file_name = "pres_ys_mean(2)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ys_old
group_plot(era5_old, ncep_r2_old,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),
                  start_year='1981',
                  end_year='2010',
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_old',
                  file_name = "pres_ys_mean(1)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_old, ncep_r2_old,
                  col_name='ys_mean',
                  y_range=(995, 1036, 5),
                  start_year='1981',
                  end_year='2010',
                  title = 'Yellow Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ys_old',
                  file_name = "pres_ys_mean(2)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ecs_present
group_plot(era5_present, ncep_r2_present,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_present',
                  file_name = "pres_ecs_mean(1)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_present, ncep_r2_present,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_present',
                  file_name = "pres_ecs_mean(2)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')
#%%
########################################################################################################ecs_new
group_plot(era5_new, ncep_r2_new,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_new',
                  file_name = "pres_ecs_mean(1)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_new, ncep_r2_new,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_new',
                  file_name = "pres_ecs_mean(2)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################ecs_old
group_plot(era5_old, ncep_r2_old,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),
                  start_year='1981',
                  end_year='2010',
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_old',
                  file_name = "pres_ecs_mean(1)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_old, ncep_r2_old,
                  col_name='ecs_mean',
                  y_range=(995,1031,5),
                  start_year='1981',
                  end_year='2010',
                  title = 'East China Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/ecs_old',
                  file_name = "pres_ecs_mean(2)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################es_present
group_plot(era5_present, ncep_r2_present,
                  col_name='es_mean',
                  y_range=(990,1035,5),
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_present',
                  file_name = "pres_es_mean(1)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_present, ncep_r2_present,
                  col_name='es_mean',
                  y_range=(990,1035,5),
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_present',
                  file_name = "pres_es_mean(2)",
                  title_suffix='1994-2023',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################es_new
group_plot(era5_new, ncep_r2_new,
                  col_name='es_mean',
                  y_range=(990,1035,5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_new',
                  file_name = "pres_es_mean(1)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_new, ncep_r2_new,
                  col_name='es_mean',
                  y_range=(990,1035,5),       
                  start_year='1991',
                  end_year='2020',
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_new',
                  file_name = "pres_es_mean(2)",
                  title_suffix='1991-2020',     
                  y_label='Sea Level Pressure[hPa]')
# %%
########################################################################################################es_old
group_plot(era5_old, ncep_r2_old,
                  col_name='es_mean',
                  y_range=(990,1035,5),
                  start_year='1981',
                  end_year='2010',
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_old',
                  file_name = "pres_es_mean(1)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')

subplot_plot(era5_old, ncep_r2_old,
                  col_name='es_mean',
                  y_range=(990,1035,5),
                  start_year='1981',
                  end_year='2010',
                  title = 'East Sea Monthly Mean Sea Level Pressure',
                  dir ='monthly_mean_present/pres/es_old',
                  file_name = "pres_es_mean(2)",
                  title_suffix='1981-2010',     
                  y_label='Sea Level Pressure[hPa]')
# %%
