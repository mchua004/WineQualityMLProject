#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
#from sqlalchemy import create_engine
import pickle
import pandas as pd
from wine_ML import wine_quality, wine_type 
from flask import Flask, render_template, request
from config import username, password

app = Flask(__name__)
#################################################
# Database Setup
#################################################

#connection_string = f'{username}:{password}@ec2-34-230-115-172.compute-1.amazonaws.com/d9p4l9mkflujo5'
#engine = create_engine(f'postgresql://{connection_string}')

# reflect an existing database into a new model
#Base = automap_base()

# reflect the tables
#Base.prepare(engine, reflect=True)

# Save reference to the table
#Master_File = Base.classes.winequality_final

# Create our session (link) from Python to the DB
#session = Session(engine)

#"""Return the data in the master_data_file table"""
# Perform a query to retrieve the data and precipitation scores
#results = session.query(Master_File.type, Master_File.fixed_acidity, Master_File.volatile_acidity, Master_File.citric_acid, Master_File.residual_sugar, 
#                        Master_File.chlorides, Master_File.free_sulfur_dioxide, Master_File.total_sulfur_dioxide, Master_File.density, Master_File.ph,
#                        Master_File.sulphates, Master_File.alcohol, Master_File.quality)

#session.close()

# Create a dictionary from the row data and append to a list of precipitation_scores
#master_file = []
#for type, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, quality in results:
#    master_file_dict = {}
#    master_file_dict["Type"] = type
#    master_file_dict["Fixed Acidity"] = fixed_acidity
#    master_file_dict["Volatile Acidity"] = volatile_acidity
#    master_file_dict["Citric Acid"] = citric_acid
#    master_file_dict["Residual Sugar"] = residual_sugar
#    master_file_dict["Chlorides"] = chlorides
#    master_file_dict["Free Sulfur Dioxides"] = free_sulfur_dioxide
#    master_file_dict["Total Sulfur Dioxide"] = total_sulfur_dioxide
#    master_file_dict["Density"] = density
#    master_file_dict["pH"] = ph
#    master_file_dict["Sulphates"] = sulphates
#    master_file_dict["Alcohol"] = alcohol
#    master_file_dict["Quality"] = quality
#    master_file.append(master_file_dict)

########################################
# CONNECTION TO THE MODELS
#######################################
path ='./lib/models/'
# descriptors that can be predicted
descriptors = ['type_red','quality']
# best model and dimension of the problem reduction
model_list = ['kNN','pca']
#dictionary containing both PCA and kNN for each descriptor
model_dic = {}
for model in model_list:
    for descriptor in descriptors:
        model_dic[f'{model}_{descriptor}'] = pickle.load(open(path+model+'_'+descriptor+'.pkl', 'rb'))
print(model_dic)

############## ONLINE APPLICATION
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(render_template('main.html'))

#Getting Form Input
    if request.method == 'POST':
        alcohol =  request.form['alcohol']
        chlorides =  request.form['chlorides']
        citric_acid =  request.form['citric_acid']
        fixed_acidity = request.form['fixed_acidity']
        free_sulfur_dioxide =  request.form['free_sulfur_dioxide']
        total_sulfur_dioxide   =  request.form['total_sulfur_dioxide']
        density      =  request.form['density']
        pH =  request.form['pH']
        residual_sugar      =  request.form['residual_sugar']
        sulphates     =  request.form['sulphates']
        volatile_acidity                  =  request.form['volatile_acidity']

    data = pd.DataFrame.from_dict({'alcohol': [alcohol],
                                    'chlorides': [chlorides],
                                    'citric_acid': [citric_acid],
                                    'fixed_acidity': [fixed_acidity],
                                    'free_sulfur_dioxide': [free_sulfur_dioxide],
                                    'total_sulfur_dioxide': [total_sulfur_dioxide],
                                    'density': [density],
                                    'pH': [pH],
                                    'residual_sugar': [residual_sugar],
                                    'sulphates': [sulphates],
                                    'volatile_acidity': [volatile_acidity]}, orient='columns')  

    # Predicting the Wine Quality using the loaded model
    result = {}
    for descriptor in descriptors:
        result[descriptor] = model_dic[f'kNN_{descriptor}'].predict(model_dic[f'pca_{descriptor}'].transform(data))
    wine_result = f"{wine_type(result['type_red']).capitalize()} wine of {wine_quality(result['quality'])}"
    return render_template('main.html', wine_result=wine_result)

if __name__ == '__main__':
    app.run(host='localhost', debug=True)