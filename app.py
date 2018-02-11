### App that utilizes results from scrape_mars.py and inserts results into a MongoDB document
# dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)    
mongo = PyMongo(mars_webscrape)

@app.route("/")
def index_pg():
