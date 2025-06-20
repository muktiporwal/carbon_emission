import pandas as pd
import numpy as np

orig_data_file=r"climate_change.xls"
data_sheet="Data"
data_orig=pd.read_excel(io=orig_data_file, sheet_name=data_sheet)

print("Shape of the original dataset: ",data_orig.shape)

print("Available columns: ",data_orig.columns)

print("Coumns data types: ",data_orig.dtypes)

print("Overview of the first 5 rows: ",data_orig.head)

print("Discriptive statistics of the columns: ",data_orig.describe())

data_orig['Series name'].unique()

data_orig['Series code'].unique()

data_orig['Decimals'].unique()

data_orig[data_orig['SCALE']=='Text']

data_orig[data_orig['Decimals']=='Text']

#data cleaning
data_clean=data_orig
print("Original number of rows: ",data_clean.shape[0])
data_clean=data_clean[data_clean['SCALE']!='Text']
print("Current number of rows: ",data_clean.shape[0])

print("Original number of columns: ",data_clean.shape[1])
data_clean=data_clean.drop(['Country name','Series code','SCALE','Decimals'],axis='columns')
print("Current number of columns: ",data_clean.shape[1])

data_clean.iloc[:,2:]=data_clean.iloc[:,2:].replace({"'":np.nan, '..':np.nan})

data_clean2=data_clean.applymap(lambda x: pd.to_numeric(x, errors='ignore'))
print("Print the column data types after transformations: ",data_clean2.dtypes)

#define shorter name corresponding to most relevant variables in a dictionary
chosen_vars={'Cereal yield (kg per hectare)': 'cereal_yield',
               'Foreign direct investment, net inflows (% of GDP)': 'fdi_perc_gdp',
               'Access to electricity (% of total population)': 'elec_access_perc',
               'Energy use per units of GDP (kg oil eq./$1,000 of 2005 PPP $)': 'en_per_gdp',
               'Energy use per capita (kilograms of oil equivalent)': 'en_per_cap',
               'CO2 emissions, total (KtCO2)': 'co2_ttl',
               'CO2 emissions per capita (metric tons)': 'co2_per_cap',
               'CO2 emissions per units of GDP (kg/$1,000 of 2005 PPP $)': 'co2_per_gdp',
               'Other GHG emissions, total (KtCO2e)': 'other_ghg_ttl',
               'Methane (CH4) emissions, total (KtCO2e)': 'ch4_ttl',
               'Nitrous oxide (N2O) emissions, total (KtCO2e)': 'n2o_ttl',
               'Droughts, floods, extreme temps (% pop. avg. 1990-2009)': 'nat_emerg',
               'Population in urban agglomerations >1million (%)': 'pop_urb_aggl_perc',
               'Nationally terrestrial protected areas (% of total land area)': 'prot_area_perc',
               'GDP ($)': 'gdp',
               'GNI per capita (Atlas $)': 'gni_per_cap',
               'Under-five mortality rate (per 1,000)': 'under_5_mort_rate',
               'Population growth (annual %)': 'pop_growth_perc',
               'Population': 'pop',
               'Urban population growth (annual %)': 'urb_pop_growth_perc',
               'Urban population': 'urb_pop'}
data_clean2['Series name']=data_clean2['Series name'].replace(to_replace=chosen_vars)

#Data frame transformations
data_clean2.head()

chosen_cols=list(chosen_vars.values())
frame_list=[]
for variables in chosen_cols:
    frame=data_clean2[data_clean2['Series name'==variables]] # type: ignore
    frame=frame.melt(id_vars=['Country code','Series name']).rename(coulmns={'Country code': 'country', 'variable': 'year', 'value': variables}).drop(['Series name'], axis='columns')
    frame_list.append(frame)

from functools import reduce
all_vars=reduce(lambda left, right: pd.merge(left, right, on=['country', 'year'], how='outer'), frame_list)

all_vars.head()
