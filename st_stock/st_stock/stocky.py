
import yfinance as yf 
import pandas as pd
from typing import Union, List, Dict


def get_assets(symbols: Union[list, str],period='1y', **kwargs):
    '''
    download stock/cryto information as pandas dateframe
    '''
    if isinstance(symbols, str):
        return yf.download(symbols, period=period, **kwargs)
    else:
        raise ValueError('You still in need to implement ')

