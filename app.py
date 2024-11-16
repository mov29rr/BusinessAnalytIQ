import streamlit as st
import pandas as pd

st.title("AnalytIQ")

products_tab, analyse_tab = st.tabs(["products", "analyse"])

with products_tab:
    st.header("Products")

    sample_data = {
        "Product": ["Computer A", "Computer B"],
        "Cost": [1000, 100],
        "Time": [4, 2],
        "Revenue": [2000, 400]
    }

    df = pd.DataFrame(sample_data)

    edited_df = st.data_editor(df, use_container_width=True)

with analyse_tab:
    st.header("Analyse")