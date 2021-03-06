from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars_4

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", dict = mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_():


    scrape_dict = mission_to_mars_4.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scrape_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
