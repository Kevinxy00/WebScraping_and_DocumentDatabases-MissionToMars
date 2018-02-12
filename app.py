### App that utilizes results from scrape_mars.py and inserts results into a MongoDB document
# dependencies
from flask import Flask, jsonify, redirect, render_template
import pymongo
from pymongo import MongoClient
from scrape_mars import scrape

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
# remember to run mongodb in gitbash or cmd line
client = MongoClient('mongodb://localhost:27017/')

# initialize flask 
app = Flask(__name__)    

# reference to mongodb collection mars_info
db = client.mars_info_DB
mars_collec = db.mars_collection

@app.route("/")
def render_index():
    # If scrape_mars() has yet to be run, will get an index error
    try:
        # find the first entry, which is where I inserted the entire python dict
        mars_find =  mars_collec.find_one() 
        # get the scrape results from mongodb collection mars_info
        # Since dot notation doesn't work with lists and calling by integers, I have to do this
        Nasa_latest_title = mars_find['Nasa_latest_title']
        Nasa_latest_paragraph1 = mars_find['Nasa_latest_paragraph'][0]
        Nasa_latest_paragraph2 = mars_find['Nasa_latest_paragraph'][1]
        featured_image_url = mars_find['featured_image_url']
        mars_weather_tweet = mars_find['mars_weather_tweet']
        mars_facts_table = mars_find['mars_facts_table']
        hemis_1_title = mars_find['hemispheres'][0]['title']
        hemis_1_img = mars_find['hemispheres'][0]['img_url']
        hemis_2_title = mars_find['hemispheres'][1]['title']
        hemis_2_img = mars_find['hemispheres'][1]['img_url']
        hemis_3_title = mars_find['hemispheres'][2]['title']
        hemis_3_img = mars_find['hemispheres'][2]['img_url']
        hemis_4_title = mars_find['hemispheres'][3]['title']
        hemis_4_img = mars_find['hemispheres'][3]['img_url']
    except (IndexError, TypeError) as e:
        # note: either error only occurs if there's nothing in the mars_info_DB. Either there's no index or NoneType object returns. 
        Nasa_latest_title = ""
        Nasa_latest_paragraph1 = ""
        Nasa_latest_paragraph2 = ""
        featured_image_url = ""
        mars_weather_tweet = ""
        mars_facts_table = ""
        hemis_1_title = ""
        hemis_1_img = ""
        hemis_2_title = ""
        hemis_2_img = ""
        hemis_3_title = ""
        hemis_3_img = ""
        hemis_4_title = ""
        hemis_4_img = ""
    return render_template("index.html", Nasa_latest_title=Nasa_latest_title, Nasa_latest_paragraph1=Nasa_latest_paragraph1,\
                            Nasa_latest_paragraph2=Nasa_latest_paragraph2, featured_image_url=featured_image_url,\
                            mars_weather_tweet=mars_weather_tweet, mars_facts_table=mars_facts_table)

# using scrape() from scrape_mars.py, inserts results into a mars_info in MongoDB
@app.route('/scrape')
def scrape_mars():
    scrape_rslts = scrape()
    mars_collec.replace_one(
        {}, # filter. {} means the whole collection
        scrape_rslts, # Replacement
        upsert=True # creates a new document when no document matches the query criteria.
    )
    return redirect('http://localhost:5000/', code=302) # redirects route back to index ('/')

if __name__ == '__main__':
    app.run()
