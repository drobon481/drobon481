#!/usr/bin/env python
# coding: utf-8

# In[53]:


def github() -> str:
    """
    Returns a link to solutions on GitHub.
    """
    return "https://github.com/drobon481/drobon481/tree/main"

print(github())


# In[54]:


import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Imports Tesla stock price history
    """
    url = "https://lukashager.netlify.app/econ-481/data/TSLA.csv"
    data = pd.read_csv(url)
    return data


data = load_data()
print(data.head())


# In[55]:


import pandas as pd
import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Plots the closing price of Tesla stock between specified start and end dates.
    """
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    filtered_data = df[(df['Date'] >= start) & (df['Date'] <= end)]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['Date'], filtered_data['Close'], label='Close Price', linewidth=2)
    plt.title(f'Tesla Stock Closing Prices from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)
    plt.legend()
  

    return None
    
# Example usage with the function defined above
plot_close(data, '2020-06-01', '2022-04-01')


# In[56]:


import pandas as pd
import statsmodels.api as sm

def autoregress(df: pd.DataFrame) -> float:
    """
    Performs an autoregressive model of order 1 on the difference between 'Close' price of a stock DataFrame and its lag,
    returns the t statistic from the regression using HC1 standard errors.
    """
    # Ensure 'Date' is a datetime for proper alignment and sorting
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Lag the 'Close' column
    df['Lag_Close'] = df['Close'].shift(1)
    
    # Calculate the difference between 'Close' and its lag
    df['Delta_Close'] = df['Close'] - df['Lag_Close']
    
    # Lag the difference
    df['Lag_Delta_Close'] = df['Delta_Close'].shift(1)
    
    # Drop NA values
    df.dropna(inplace=True)
    
    # Prepare the regressor and dependent variable
    X = df['Lag_Delta_Close']
    y = df['Delta_Close']
    
    # Fit the regression model
    model = sm.OLS(y, X).fit(cov_type='HC1')  # Using HC1 robust standard errors
    
    # Retrieve the t-statistic for the coefficient (of Lag_Delta_Close)
    t_stat = model.tvalues[0]  # Assuming 'Lag_Delta_Close' is the only predictor and no intercept
    
    return t_stat

# Example usage:
data = load_data()  # Assuming 'load_data' function is defined as per earlier instructions
t_statistic = autoregress(data)
print(f'T-statistic from the regression: {t_statistic}')



# In[57]:


import pandas as pd
import statsmodels.api as sm
import numpy as np

def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Performs logistic regression to predict the probability of the change in closing price being greater than 0,
    returns the t statistic for the coefficient B0.
    """
    # Ensure 'Date' is a datetime for proper alignment and sorting
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Lag the 'Close' column
    df['Lag_Close'] = df['Close'].shift(1)
    
    # Calculate the difference between 'Close' and its lag
    df['Delta_Close'] = df['Close'] - df['Lag_Close']
    
    # Lag the difference
    df['Lag_Delta_Close'] = df['Delta_Close'].shift(1)
    
    # Create a binary variable indicating whether the change is greater than 0
    df['Positive_Change'] = (df['Delta_Close'] > 0).astype(int)

    # Drop NA values
    df.dropna(subset=['Lag_Delta_Close', 'Positive_Change'], inplace = True)
    
    # Fit logistic regression model
    X = df['Lag_Delta_Close']
    y = df['Positive_Change']  # Target variable
    
    model = sm.Logit(y, X).fit()
    
    # Retrieve the t-statistic for the coefficient (of the constant/B0)
    t_stat = model.tvalues['Lag_Delta_Close']

    return t_stat

# Example usage:
data = load_data()  # Assuming 'load_data' function is defined as per earlier instructions
t_statistic = autoregress_logit(data)
print(f'T-statistic from the logistic regression: {t_statistic}')


# In[58]:


import pandas as pd
import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    """
    Plots the daily changes in the closing price of Tesla stock.
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Compute daily changes in the 'Close' price
    df['Delta_Close'] = df['Close'].diff()
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Delta_Close'], label='Daily Change in Close Price', linewidth=1.5, color='blue')
    plt.title('Daily Change in Tesla Stock Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Change in Closing Price (USD)')
    plt.grid(True)
    plt.legend()

    return None

data = load_data()  # Assuming 'load_data' function is defined as per earlier instructions
plot_delta(data)


# In[ ]:




