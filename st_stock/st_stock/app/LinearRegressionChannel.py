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


def plot_linear_regression_channel(symbol: str, period='1y'):
    '''
    Plot linear regression channel for a given asset 
    '''
    df = get_assets(symbol, period)
    df = df.reset_index()
    df['epoch'] = (df.Date - datetime(1970,1,1)).dt.total_seconds()
    sns.set(font_scale=1.5)

    fig, ax = plt.subplots(figsize=(15, 8))
    ## using build in the regression plot
    rp = sns.regplot(list(range(len(df))), df.Close, ci=95, marker='.', ax=ax)
    ## extract the regression list 
    y_rp = rp.get_lines()[0].get_ydata()
    x_rp = rp.get_lines()[0].get_xdata()
    ## plot the channel
    sns.lineplot(x=x_rp, y=y_rp + np.std(y_rp), color='r', ax=ax)
    sns.lineplot(x=x_rp, y=y_rp - np.std(y_rp), color='r', ax=ax)
    return fig, ax 

def st_linear_regression_channel():
    config = load_config()
    symbol =  st.sidebar.selectbox('symbols', load_cypto_symbols()) 
    period = st.sidebar.selectbox('Period', config['cypto']['periods'])
    ## TODO: add intervals

    st.header('Linear Regression Channels for cypto')
    st.write(plot_linear_regression_channel(symbol, period)[0])
