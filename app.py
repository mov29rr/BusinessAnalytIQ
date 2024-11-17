from portfolio_analysis import InvestmentCloud, calculate_optimal_asset_dist, display_assets_pie, NonFeasibleSolutionError
from flask import Flask, render_template, Response

app = Flask(__name__)

investment_clouds = [
    InvestmentCloud("S&P 500", 0.15, .10, .55),
    InvestmentCloud("Apple", 0.2, .11, .50),
    InvestmentCloud("Microsoft", 0.3, .05, .50),
    InvestmentCloud("Facebook", 0.1, .50, .60)
]

@app.route("/asset_dist.png")
def asset_dist():
    try:
        optimised_asset_dist = calculate_optimal_asset_dist(investment_clouds)
        img = display_assets_pie(optimised_asset_dist)

        return Response(img, mimetype="image/png")
    except NonFeasibleSolutionError:
        # TODO: Error
        pass

@app.route("/")
def index():
    return render_template("portfolio.html", investment_clouds=investment_clouds)

if __name__ == '__main__':
    app.run(debug=True)