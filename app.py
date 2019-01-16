import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, select
from flask import Flask, jsonify, render_template
import datetime as dt
from sqlalchemy import desc
import json

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)

query=session.query(Measurement).order_by(desc(Measurement.date)).limit(1)

df = pd.read_sql(query.statement, query.session.bind)
lastDate = df.iloc[0]['date']
# Calculate the date 1 year ago from the last data point in the database
ySplit = lastDate.split('-')

fDate=int(ySplit[0]) - 1
fDay=int(ySplit[1])-1
fDate=str(fDate)
fDate1= fDate+"-0"+str(fDay)+"-"+str(ySplit[2])
@app.route("/")
def index():
    """Return the homepage."""
    return "hello"

@app.route("/api/v1.0/precipitation")
def apiPrecipitation():
	
	yQuery=session.query(Measurement).filter(and_(Measurement.date >= fDate1, Measurement.date <= lastDate)).order_by(desc(Measurement.date))
	df = pd.read_sql(yQuery.statement, yQuery.session.bind)
	dfDP=pd.DataFrame(df,columns=['date', 'tobs'])
	dfDP.set_index('date', inplace=True)
	jsonfiles = json.loads(dfDP.to_json(orient='table'))

	return jsonify(jsonfiles)


@app.route("/api/v1.0/stations")
def apiStations():
	
	yQuery=session.query(Station)
	df = pd.read_sql(yQuery.statement, yQuery.session.bind)

	jsonfiles = json.loads(df.to_json(orient='records'))

	return jsonify(jsonfiles)

@app.route("/api/v1.0/tobs")
def apiTobs():
	
	yQuery=session.query(Measurement).filter(and_(Measurement.date >= fDate1, Measurement.date <= lastDate)).order_by(desc(Measurement.date))
	df = pd.read_sql(yQuery.statement, yQuery.session.bind)
	dfDP=pd.DataFrame(df,columns=['date', 'tobs'])
	dfDP.set_index('date', inplace=True)
	jsonfiles = json.loads(dfDP.to_json(orient='records'))

	return jsonify(jsonfiles)
@app.route("/api/v1.0/date/<start>")
def apiDates2(start):
	
	yQuery=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
	.filter(Measurement.date >= start)
	print(start)

	df = pd.read_sql(yQuery.statement, yQuery.session.bind)
	jsonfiles = json.loads(df.to_json(orient='records'))

	return jsonify(jsonfiles)

@app.route("/api/v1.0/date/<start>/<end>")
def apiDates(start,end):
	
	if(end != ''):
		print(start,end)
		yQuery=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
		.filter(and_(Measurement.date >= start, Measurement.date <= end))
	else:
		yQuery=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
		.filter(Measurement.date >= start)
		print(start)

	df = pd.read_sql(yQuery.statement, yQuery.session.bind)
	jsonfiles = json.loads(df.to_json(orient='records'))

	return jsonify(jsonfiles)
if __name__ == "__main__":
    app.run()


