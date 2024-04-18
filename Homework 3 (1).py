#!/usr/bin/env python
# coding: utf-8

# In[47]:


def github() -> str:
    """
    Returns a link to solutions on GitHub.
    """
    return "https://github.com/drobon481/drobon481/tree/main"

print(github())


# In[49]:


import pandas as pd

all_data = []
def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Imports yearly data from EPA Excel sheets for the specified years.
    """
   
    base_url = "https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"

    for year in years:
        url = base_url.format(year=year)  # Constructs the URL for the current year
        data = pd.read_excel(url, sheet_name='Direct Emitters', skiprows=3, header=0)
        data['year'] = year  # Add a column for the year
        all_data.append(data)

    return pd.concat(all_data, ignore_index=True)

years = [2019, 2020, 2021, 2022]
emissions_data = import_yearly_data(years)
print(emissions_data.head())



# In[50]:


import pandas as pd
import pyxlsb

parent_data = []
def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Imports data from different tabs of a single 'Parent Companies' Excel sheet.
    """
   
    file_url = "https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"

    for year in years:
        data = pd.read_excel(file_url, sheet_name=str(year))  # Read data from the tab named as the year
        data['year'] = year  # Add a column for the year
        parent_data.append(data)
        
    return pd.concat(parent_data)

years = [2019, 2020, 2021, 2022]
parent_data = import_parent_companies(years)
parent_data.dropna(how = 'all')
print(parent_data.head())


# In[51]:


import pandas as pd

def n_null(df: pd.DataFrame, column: str) -> int:
    """
    Count the number of null values in a specified column of a DataFrame.
    """
    return df[column].isnull().sum()

null_count = n_null(parent_data, 'FRS ID (FACILITY)')
print(null_count)


# In[44]:


import pandas as pd

def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and merges emissions and parent companies data.
    """
    # Left join the parent companies data onto the EPA data using as join keys the year and Facility ID variables
    merged_data = pd.merge(emissions_data, parent_data, 
                           left_on=['year', 'Facility Id'], 
                           right_on=['year', 'GHGRP FACILITY ID'], 
                           how='left')
    
    # Subset the data to the required variables
    subset_columns = ['Facility Id', 'year', 'State', 'Industry Type (sectors)', 
                      'Total reported direct emissions', 'PARENT CO. STATE', 'PARENT CO. PERCENT OWNERSHIP']
    cleaned_data = merged_data[subset_columns]
    
    # Make all column names lower-case
    cleaned_data.columns = cleaned_data.columns.str.lower()

    return cleaned_data

cleaned_df = clean_data(emissions_data, parent_data)
print(cleaned_df.head())


# In[46]:


import pandas as pd

def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Aggregates emissions data by specified group variables and calculates
    minimum, median, mean, and maximum values for total reported direct emissions
    and parent company percent ownership.
    """
    # Aggregate the data
    agg_data = df.groupby(group_vars).agg({
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    })

    agg_data = agg_data.sort_values(by=('total reported direct emissions', 'mean'), ascending=False)

    return agg_data

agg_df = aggregate_emissions(cleaned_df, group_vars=['industry type (sectors)'])
print(agg_df.head())


# In[ ]:




