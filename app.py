from portfolio_analysis import InvestmentCloud, calculate_optimal_asset_dist, display_assets_pie, NonFeasibleSolutionError
from pymongo import MongoClient
from flask import Flask, render_template, Response

#Database client url
uri = "mongodb+srv://rwomack1325:esMBO1BvvqjzpReA@maindb.rluzm.mongodb.net/?retryWrites=true&w=majority&appName=MainDB"
client = MongoClient(uri)

#Database being searched
database = client.get_database("AnalytIQDB")

#Collection(s)/table(s) being searched
assetsCollection = database.get_collection("Assets")

#Raw Data from DB
listofRawAssets = assetsCollection.distinct("asset")
listofRawER = assetsCollection.distinct("expected return")
listofRawMin = assetsCollection.distinct("minimum investment")
listofRawMax = assetsCollection.distinct("maximum investment")

#Sanitising the data, putting it in lists
sanitisedAssets = [str(asset).strip("[]\"\'") for asset in listofRawAssets]
sanitisedER = [float(er) for er in listofRawER]
sanitisedMin = [float(min) for min in listofRawMin]
sanitisedMax = [float(max) for max in listofRawMax]

#Counting records
record_count = min(len(sanitisedAssets), len(sanitisedER), len(sanitisedMin), len(sanitisedMax))

app = Flask(__name__)

#List of investments
investment_clouds = []

#Add assets from DB to list of investments
for i in range(record_count):
    investment_clouds.append(InvestmentCloud(sanitisedAssets[i], sanitisedER[i], sanitisedMin[i], sanitisedMax[i]))
    i += 1

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