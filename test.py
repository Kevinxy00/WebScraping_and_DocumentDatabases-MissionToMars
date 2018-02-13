# dependencies
from flask import Flask, jsonify, redirect, render_template
import pymongo
from pymongo import MongoClient
from scrape_mars import scrape
import pprint
# remember to run mongodb in gitbash or cmd line
client = MongoClient('mongodb://localhost:27017/')

# initialize flask 
app = Flask(__name__)    

# reference to mongodb collection mars_info
db = client.mars_info_DB
mars_collec = db.mars_collection

test = mars_collec.find_one()
table = test['mars_facts_table']

print(table.html)
