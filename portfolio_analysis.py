from pulp import LpMaximize, LpProblem, LpVariable, LpStatus
import matplotlib.pyplot as plt
import io

class NonFeasibleSolutionError(Exception):
    def __init__(self):
        pass

class InvalidInvestmentCloudParameterError(Exception):
    def __init__(self):
        pass

class InvestmentCloud:
    def __init__(self, asset, expected_return, minimum, maximum):
        if minimum < 0 or minimum > maximum or maximum > 1:
            raise InvalidInvestmentCloudParameterError()

        self.asset = asset
        self.expected_return = expected_return
        self.minimum = minimum
        self.maximum = maximum

class AssetDist:
    def __init__(self, name, proportion):
        self.name = name
        self.proportion = proportion

def calculate_optimal_asset_dist(investment_clouds):
    model = LpProblem("Total expected return", LpMaximize)

    asset_dists = [LpVariable(investment_cloud.asset, lowBound=0) for investment_cloud in investment_clouds]
    model += sum(asset_dists[i] * investment_clouds[i].expected_return for i in range(len(investment_clouds)))

    for i in range(len(investment_clouds)):
        model += investment_clouds[i].minimum <= asset_dists[i]
        model += investment_clouds[i].maximum >= asset_dists[i]

    model += sum(asset_dist for asset_dist in asset_dists) == 1

    model.solve()

    if LpStatus[model.status] != "Optimal":
        raise NonFeasibleSolutionError()

    return [ AssetDist(asset_dist.name, asset_dist.value()) for asset_dist in asset_dists ]

def rgb_component(status):
    return "CC" if status else "33"
def is_white(r, g, b):
    return r == 1 and g == 1 and b == 1
def is_black(r, g, b):
    return r == 0 and g == 0 and b == 0

def display_assets_pie(assets):
    labels = [ asset.name for asset in assets ]
    proportions = [ asset.proportion * 100 for asset in assets ]
    rgb_binary_combinations = [ (r, g, b) for b in [0, 1] for g in [0, 1] for r in [0, 1] if not is_white(r, g, b) and not is_black(r, g, b)]
    # TODO: Repeat colours
    colors = [ f"#{rgb_component(rgb[0])}{rgb_component(rgb[1])}{rgb_component(rgb[2])}" for rgb in rgb_binary_combinations ]

    fig, ax = plt.subplots()
    ax.pie(proportions, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, textprops={"color": "white"})
    fig.patch.set_facecolor("none")

    ax.axis("equal")

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)  # Rewind the buffer to the beginning

    return img