## Linear Regression Channel

## Ref https://medium.com/coinmonks/trading-bitcoin-with-linear-regression-channels-b84e7e43d984 

from google.protobuf import symbol_database
from st_stock.stocky import get_assets
from typing import List
from datetime import datetime 
import seaborn as sns
from matplotlib import pyplot as plt 
import numpy as np
import streamlit as st
from st_stock.misc import load_cypto_symbols, load_config

def std_line_plot(x, y, ax, sigma=1, color='r', **kwargs):
    '''
    plot strand dev lines for X sigma
    '''
    sns.lineplot(
        x = x, y = (y + (sigma * np.std(y,))), color=color, ax=ax, **kwargs)
    sns.lineplot(
        x = x, y = (y - (sigma * np.std(y))), color=color, ax=ax, **kwargs)
    return ax 

def plot_linear_regression_channel(symbol: str,  period: str='ytd', interval: str='1d', y: str='Close',):
    '''
    Plot linear regression channel for a given asset 
    '''
    df = get_assets(symbol, period, interval=interval)
    df = df.reset_index()
    df.loc[:,'idx'] = range(len(df))
    df['pct'] = df.Close.pct_change(fill_method='ffill')
    df['log'] = np.log(df.Close) 

    if 'Date' in df:
        df = df.rename(columns={'Date': 'Datetime'})
    #     # df['epoch'] = (df.Datetime - datetime(1970,1,1)).dt.total_seconds()
    #     df['']
    # else:
    #     df['epoch'] = (df.Date - datetime(1970,1,1)).dt.total_seconds()
    sns.set(font_scale=1.5)

    fig, ax = plt.subplots(figsize=(15, 8))
    ## using build in the regression plot
    reg_plot = sns.regplot(
        'idx',
        y,
        data=df,
        ci=95, marker='.',
        ax=ax,

        )
    ## extract the regression list 
    y_mean = reg_plot.get_lines()[0].get_ydata()
    x_mean = reg_plot.get_lines()[0].get_xdata()
    ## plot the channel
    std_line_plot(x_mean,y_mean, ax=ax, sigma=1, color='r', label='1 std ' )
    std_line_plot(x_mean,y_mean, ax=ax, sigma=2, color='r', linestyle='--', label='2 std' )
    # ax.set_xticklabels([datetime.fromtimestamp(x) for x in ax.get_xticks()], rotation =90)
    # print([x for x in ax.get_xticks()])
    # ax.set_xticklabels([df.loc[int(x), 'Datetime'] if x >=0 else df.loc[0,'Datetime']   for x in ax.get_xticks() ], rotation =90)
    ax.set(xlabel='')
    ax.legend()
    return (fig, ax, df)

def st_linear_regression_channel():
    config = load_config()
    symbol =  st.sidebar.selectbox('symbols', load_cypto_symbols()) 
    period = st.sidebar.selectbox('Period', config['cypto']['periods'], index=config['cypto']['periods'].index('ytd') )
    interval = st.sidebar.selectbox('Interval', config['cypto']['intervals'], index=config['cypto']['intervals'].index('1d'))
    y = st.sidebar.selectbox('Y axis', ['Close', 'pct', 'log'], index=0)

    st.header('Linear Regression Channels for cypto')
    fig, ax, data = plot_linear_regression_channel(symbol, period, interval, y=y)
    st.write(fig)
    st.dataframe(data)
