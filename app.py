import portfolio_tab
import account_tab

import streamlit as st

st.title("AnalytIQ")

portfolio_tab_handle, account_tab_handle = st.tabs(["Portfolio", "Account"])

with portfolio_tab_handle:
    portfolio_tab.render()

with account_tab_handle:
    account_tab.render()