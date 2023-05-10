# Import the dependencies.



import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp_results =  session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).all()

    session.close()

    prcp_list = list(np.ravel(prcp_results))

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_results =  session.query(Station.station, Station.name).all()

    session.close()

    station_list = list(np.ravel(station_results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs_results =  session.query(Measurement.tobs).\
                    filter(Measurement.station =='USC00519281').\
                    filter(Measurement.date >= year_ago).all()

    session.close()

    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def temp_results(start, end):
    session = Session(engine)

    stat_results =  session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    stats_list = list(np.ravel(stat_results))

    return jsonify(stats_list)

if __name__ == "__main__":
    app.run(debug=True)

    