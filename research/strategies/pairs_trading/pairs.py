import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from tqdm import tqdm

from research.datasets import CRSP
from research.datasets.config import DATA_DIR

PAIRS_PATH = DATA_DIR + "/pairs.csv"
MSE_PATH = DATA_DIR + "/mse.csv"
YEARLY_PAIRS_PATH = DATA_DIR + "/yearly_pairs.csv"

crsp = CRSP()

df = crsp.df[['permno', 'date', 'ticker', 'prc', 'ret']].copy()

df = df.query("prc > 5").reset_index(drop=True)

# Add extra date variables
df['mdt'] = df['date'].dt.strftime("%Y-%m")
df['year'] = df['date'].dt.strftime("%Y")
df['month'] = df['date'].dt.strftime("%m")

# Calculate Different Return Variables

holding_period = 6 # Alternative is 1
holding_period_var = f'ret_{holding_period}'

# Log Returns
df['logret'] = np.log1p(df['ret'])
df['cumret'] = df.groupby(['permno','year'])['logret'].cumsum().reset_index(drop=True)
df['cumret_lag'] = df.groupby('permno')['cumret'].shift(1)

# Holding period returns
df[holding_period_var] = df.groupby('permno')['logret'].rolling(holding_period,holding_period).sum().reset_index(drop=True)
df[holding_period_var] = df.groupby('permno')[holding_period_var].shift(-(holding_period-1))

pivot = df.groupby(['permno','date'])['cumret_lag'].mean().reset_index().pivot(index='date', columns='permno', values='cumret_lag')
pivot['year'] = pivot.index.year
pivot

years = pivot['year'].unique()  # [2017, 2018]

mse_frame = pd.DataFrame(index=years, columns=pivot.columns[:-1], data=float("inf"))
pairs_frame = pd.DataFrame(index=years, columns=pivot.columns[:-1], data=None)

# Iterated through each year of data
for year in tqdm(years, desc='Processing years'):
    slice = pivot[pivot['year'] == year].dropna(axis=1, how='all').drop(columns=['year'])
    
    returns = slice.dropna(axis=1).T.dropna().T # This gets rid of stocks without 12 months of returns
    returns_array = returns.values
    
    # Loop through all combination of pairs
    for i, j in combinations(range(returns_array.shape[1]), 2):
        stock_i = returns.columns[i]
        stock_j = returns.columns[j]
        
        stock_i_returns = returns_array[:, i]
        stock_j_returns = returns_array[:, j]

        mse = np.mean((stock_i_returns - stock_j_returns) ** 2)

        # Keep pairs with the lowest MSE
        if mse < mse_frame.at[year, stock_i]:
            mse_frame.at[year, stock_i] = mse
            pairs_frame.at[year, stock_i] = returns.columns[j]

pairs_frame.to_csv(PAIRS_PATH)
mse_frame.to_csv(MSE_PATH)

pairs_frame = pd.read_csv(PAIRS_PATH, index_col=0)
mse_frame = pd.read_csv(MSE_PATH, index_col=0)

# Reformat mse and pairs dataframes
result_pairs_frame = pairs_frame.unstack().reset_index().rename(columns={'level_0': 'permno','level_1': 'year', 0: 'pair'})
result_mse_frame = mse_frame.unstack().reset_index().rename(columns={'level_0': 'permno','level_1':'year', 0: 'mse'})

# Merge
merged = result_mse_frame.merge(result_pairs_frame, on=['permno','year'], how='left')

# Clean up final dataframe
merged = merged.sort_values(by=['year','mse'], ascending=True).dropna().reset_index(drop=True)

merged['permno'] = merged['permno'].astype(int)
merged['pair'] = merged['pair'].astype(int)

merged.to_csv(YEARLY_PAIRS_PATH, index=False)
