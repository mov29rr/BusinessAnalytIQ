from random import sample

import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

class CalculatedAssetDist:
    def __init__(self, name, proportion):
        self.name = name
        self.proportion = proportion

def render():
    st.header("Portfolio")

    table = {
        "Asset": ["S&P 500", "Apple", "Microsoft", "Facebook"],
        "Expected return": [0.15, 0.2, 0.3, 0.1],
        "Minimum investment": [35, 60, 30, 25],
        "Maximum investment": [5, 55, 50, 60]
    }

    df = pd.DataFrame(table)

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Optimise portfolio"):
        optimised_asset_dist = calculate_optimal_asset_dist(table)
        display_assets_pie(optimised_asset_dist)

def calculate_optimal_asset_dist(table):
    asset_names = table["Asset"]
    return [ CalculatedAssetDist(asset_names[i], 25) for i in range(len(asset_names)) ]

def display_assets_pie(assets):

    labels = [ asset.name for asset in assets ]
    sizes = [ asset.proportion for asset in assets ]
    # TODO: Randomise color generation
    colors = ["#ff9999","#66b3ff","#99ff99","#ffcc99"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, textprops={"color": "white"})
    fig.patch.set_facecolor("none")

    ax.axis("equal")

    st.pyplot(fig)