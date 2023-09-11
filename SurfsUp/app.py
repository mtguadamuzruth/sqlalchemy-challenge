# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine) 
prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
prev_year
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement =Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app =Flask(__name__)
@app.route("/")
def list_routes():
    return """<ul><li>/api/v1.0/precipitation</li><li>/api/v1.0/stations</li><li>
    /api/v1.0/tobs</li><li>/api/v1.0/:start</li><li>/api/v1.0/:start/:end</li></ul>"""
@app.route("/api/v1.0/precipitation")
def get_precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=prev_year).all()
    data= {}
    for item in results:
        data[item [0]]= item[1]
    return jsonify(data)  

@app.route("/api/v1.0/stations")
def get_stations():
    results = session.query(Measurement.station, func.count (Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    data= {}
    for item in results:
        data[item [0]]= item[1]
    return jsonify(data)  
@app.route("/api/v1.0/tobs")
def get_tobs():
    results = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= prev_year).all()
    print(results)
    return [x [0] for x in results]
#################################################
# Flask Routes
#################################################
