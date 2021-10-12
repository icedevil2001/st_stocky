import streamlit as st

st.sidebar.subheader('Options')

## pages:
## TODO: change to streamlit sessions
page = st.sidebar.selectbox('Page', ['Regression Channels'])

## make a dict lookup
if page == 'Regression Channels':
    from st_stock.app.LinearRegressionChannel import st_linear_regression_channel
    st_linear_regression_channel()


