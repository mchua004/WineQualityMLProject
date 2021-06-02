import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from config import username, password

#################################################
# Database Setup
#################################################

connection_string = f'{username}:{password}@ec2-34-230-115-172.compute-1.amazonaws.com/d9p4l9mkflujo5'
engine = create_engine(f'postgresql://{connection_string}')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Master_File = Base.classes.winequality_final

import json
import pandas as pd

# Create our session (link) from Python to the DB
session = Session(engine)

"""Return the data in the master_data_file table"""
# Perform a query to retrieve the data and precipitation scores
results = session.query(Master_File.type, Master_File.fixed_acidity, Master_File.volatile_acidity, Master_File.citric_acid, Master_File.residual_sugar, 
                        Master_File.chlorides, Master_File.free_sulfur_dioxide, Master_File.total_sulfur_dioxide, Master_File.density, Master_File.ph,
                        Master_File.sulphates, Master_File.alcohol, Master_File.quality)

session.close()

# Create a dictionary from the row data and append to a list of precipitation_scores
master_file = []
for type, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, quality in results:
    master_file_dict = {}
    master_file_dict["Type"] = type
    master_file_dict["Fixed Acidity"] = fixed_acidity
    master_file_dict["Volatile Acidity"] = volatile_acidity
    master_file_dict["Citric Acid"] = citric_acid
    master_file_dict["Residual Sugar"] = residual_sugar
    master_file_dict["Chlorides"] = chlorides
    master_file_dict["Free Sulfur Dioxides"] = free_sulfur_dioxide
    master_file_dict["Total Sulfur Dioxide"] = total_sulfur_dioxide
    master_file_dict["Density"] = density
    master_file_dict["pH"] = ph
    master_file_dict["Sulphates"] = sulphates
    master_file_dict["Alcohol"] = alcohol
    master_file_dict["Quality"] = quality
    master_file.append(master_file_dict)