import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy import create_engine

from flask import Response,json

from flask import Flask, jsonify

from flask_cors import CORS, cross_origin

from flask import Flask, render_template

# from entrancekey import postgresqlkey


#################################################
# Database Setup
#################################################

# Creating a search engine
engine = create_engine(f'postgresql+psycopg2://postgres:xxxxxx@localhost:5433/coffeeworld')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

results = engine.execute("SELECT  * FROM coffeequality").fetchall()

new = []

for i in results:
    a = {"species":i[0],"country":i[1],"harvest_year":i[2],"aroma":i[3],"cupper_points":i[4],"sweetness":i[5],"clean_cup":i[6],"uniformity":i[7],"balance":i[8],"body":i[9],"acidity":i[10],"aftertaste":i[11],"flavor":i[12],"total_cup_points":i[13]}
    new.append(a)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coffeedata", methods=["GET"])
def welcome():
    """List all available api routes."""
    
    return (json.dumps(new))


if __name__ == '__main__':
    app.run(debug=True)
