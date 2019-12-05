from flask import Flask, render_template
import pymongo
import scrape_mars


conn="mongodb://localhost:27017"
client=pymongo.MongoClient(conn)
db=client.mars_db


app = Flask(__name__)

@app.route("/")
def index():
    mars_data=scrape_mars.scrape_all()
    db.mars.delete_many({})
    db.mars.insert_many([mars_data])
    return render_template("index.html",mars=mars_data)

@app.route("/scrape")
def scraper():
    mars_data=scrape_mars.scrape_all()
    db.mars.delete_many({})
    db.mars.insert_many([mars_data])
    return('Done!')


if __name__ == "__main__":
    app.run()