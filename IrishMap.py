"""
Created on Fri Feb  5 18:48:07 2021/ @ Dublin, Ireland

@author: Saeed Misaghian
Email: sam.misaqian@gmail.com 

"""
import pandas as pd
path = 'C:/Users/map/'
df = pd.read_csv(path+'Tdata.csv')

import geopandas as gpd
ROI_map= gpd.read_file(path+'IRL_adm1.shp')
ROI_map=ROI_map.set_index('NAME_1')
df=df.set_index('County')
df2= ROI_map.join(df)
# we need to replace NaN rows with 0 since there are some counties without any wind turbines 
df2['Installed Capacity (MW)']=df2['Installed Capacity (MW)'].fillna(value=0)
df2['No of Turbines']=df2['No of Turbines'].fillna(value=0)
df2['name1'] = df2.index
MAP=df2
#MAP['test2']=MAP['No of Turbines']/189
variable = 'Installed Capacity (MW)'
vmin, vmax = 0, 500
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8,10),facecolor='lightsteelblue')
fig=MAP.plot(column='Installed Capacity (MW)', cmap='YlGn', linewidth=0.8, ax=ax, edgecolor='#140656',facecolor='lightslategray',vmin=vmin, vmax=vmax,
legend=True, norm=plt.Normalize(vmin=vmin, vmax=vmax))
ax.axis('off')
ax.annotate('Installed Capacity (MW)',xy=(0.9, .65),rotation=270, xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='black')

#Getting the lan and lat here from geometry data    
MAP['coords']=MAP['geometry'].apply(lambda x: x.representative_point().coords[:])
MAP['coords']=[coords[0] for coords in MAP['coords']]

from random import gauss

# Add turbine numbers here
for idx, row in df2.iterrows():
    if row['No of Turbines']!=0:
        s=row['No of Turbines']
        ss=int(s)
        for i in list(range(ss)):
            z=row['No of Turbines']/1000+gauss(0, 0.1)
            plt.scatter(x=z+row['coords'][0],y=gauss(0, 0.03)+row['coords'][1],c='#ec1313',alpha=0.5)

#Add names of county here
for idx, row in MAP.iterrows():
    plt.annotate(s=row['name1'], xy=row['coords'],
                 horizontalalignment='center', color='black',fontsize=10, fontweight='light')
    
import os 
path2='C:/Users/map/'
filepath = os.path.join(path2,'IrishMap.jpg')
chart = fig.get_figure()
chart.savefig(filepath, dpi=300)












