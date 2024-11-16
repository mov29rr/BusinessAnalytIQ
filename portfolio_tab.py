from random import sample

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

def render():
    st.header("Portfolio")

    assets = {
        "Asset": ["S&P 500", "APPL"],
        "Expected return": [0.15, 0.2],
        "Minimum investment": [35, 60],
        "Maximum investment": [25, 55]
    }

    df = pd.DataFrame(assets)

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Optimise portfolio"):
        for x in assets:
            print(x)

        labels = ["Category A", "Category B", "Category C", "Category D"]
        sizes = [15, 30, 45, 10]
        colors = ["#ff9999","#66b3ff","#99ff99","#ffcc99"]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)

        ax.axis("equal")

        st.pyplot(fig)