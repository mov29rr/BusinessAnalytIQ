from random import sample

import streamlit as st
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable

import matplotlib.pyplot as plt

class InvestmentCloud:
    def __init__(self, asset, expected_return, minimum, maximum):
        self.asset = asset
        self.expected_return = expected_return
        self.minimum = minimum
        self.maximum = maximum

class AssetDist:
    def __init__(self, name, proportion):
        self.name = name
        self.proportion = proportion

def render():
    st.header("Portfolio")

    # TODO: DB connection
    investment_clouds = [
        InvestmentCloud("S&P", 0.15, 35, 5),
        InvestmentCloud("Apple", 0.2, 40, 50),
        InvestmentCloud("Microsoft", 0.3, 30, 50),
        InvestmentCloud("Facebook", 0.1, 25, 60)
    ]
    table = {
        "Asset": [ investment_cloud.asset for investment_cloud in investment_clouds ],
        "Expected return": [ investment_cloud.expected_return for investment_cloud in investment_clouds ],
        "Minimum investment": [ investment_cloud.minimum for investment_cloud in investment_clouds ],
        "Maximum investment": [ investment_cloud.maximum for investment_cloud in investment_clouds ]
    }

    df = pd.DataFrame(table)

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Optimise portfolio"):
        optimised_asset_dist = calculate_optimal_asset_dist(investment_clouds)
        display_assets_pie(optimised_asset_dist)

def calculate_optimal_asset_dist(investment_clouds):
    model = LpProblem("Total expected return", LpMaximize)

    asset_dists = [LpVariable(investment_cloud.asset, lowBound=0) for investment_cloud in investment_clouds]
    model += sum(asset_dists[i] * investment_clouds[i].expected_return for i in range(len(investment_clouds)))

    for i in range(len(investment_clouds)):
        model += investment_clouds[i].minimum <= asset_dists[i]
        model += investment_clouds[i].maximum >= asset_dists[i]

    model += sum(asset_dist for asset_dist in asset_dists) == 100

    model.solve()

    return [ AssetDist(asset_dist.name, asset_dist.value()) for asset_dist in asset_dists ]

def display_assets_pie(assets):

    labels = [ asset.name for asset in assets ]
    sizes = [ asset.proportion for asset in assets ]
    # TODO: Randomise color generation
    colors = ["#ff9999","#66b3ff","#99ee99","#ffcc99"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, textprops={"color": "white"})
    fig.patch.set_facecolor("none")

    ax.axis("equal")

    st.pyplot(fig)