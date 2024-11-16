from random import sample

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

def render():
    st.header("Portfolio")

    assets = {
        "Asset": ["S&P 500", "Apple", "Microsoft", "Facebook"],
        "Expected return": [0.15, 0.2, 0.3, 0.1],
        "Minimum investment": [35, 60, 30, 25],
        "Maximum investment": [5, 55, 50, 60]
    }

    df = pd.DataFrame(assets)

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Optimise portfolio"):
        labels = [ asset for asset in assets["Asset"] ]

        # TODO: Calculate actual distributions
        sizes = [15, 30, 45, 10]
        colors = ["#ff9999","#66b3ff","#99ff99","#ffcc99"]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, textprops={"color": "white"})
        fig.patch.set_facecolor("none")

        ax.axis("equal")

        st.pyplot(fig)