#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
#from sqlalchemy import create_engine
import pickle
import pandas as pd
from wine_ML import wine_quality, wine_type, plotly_figure_type, new_dataframe, rm_tmp_file 
from flask import Flask, render_template, request
from os import path


app = Flask(__name__)

########################################
# CONNECTION TO THE MODELS
#######################################
directory ='./lib/models/'
# descriptors that can be predicted
descriptors = ['type_red','quality']
# best model and dimension of the problem reduction
model_list = ['kNN','pca']
#dictionary containing both PCA and kNN for each descriptor
model_dic = {}
for model in model_list:
    for descriptor in descriptors:
        model_dic[f'{model}_{descriptor}'] = pickle.load(open(directory+model+'_'+descriptor+'.pkl', 'rb'))
print(model_dic)
###################################################
# READING THE CSV FILE CONTAINING THE MODELED DATA
##################################################
df_init = pd.read_csv(f'lib/data/winequality-final.csv')

############## ONLINE APPLICATION
@app.route('/')
def home():
    rm_tmp_file()
    return(render_template('home.html'))

@app.route('/about')
def about():
    rm_tmp_file()
    return(render_template('about.html'))

@app.route('/data_analysis')
def data_analysis():
    rm_tmp_file()
    return(render_template('analysis.html'))

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
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
        
        
        if path.exists('lib/data/winequality-flask.csv'):
            df = pd.read_csv('lib/data/winequality-flask.csv')
        else:
            df = df_init
        # dimension reduction of the dataframe
        X_df = model_dic['pca_type_red'].transform(df.drop(columns=['type','quality']))
        # Predicting the Wine Quality using the loaded model
        result = {}
        for descriptor in descriptors:
            result[descriptor] = model_dic[f'kNN_{descriptor}'].predict(model_dic[f'pca_{descriptor}'].transform(data))
        wine_result = f"{wine_type(result['type_red']).capitalize()} wine of {wine_quality(result['quality'])}"
        graphJson = plotly_figure_type(X_df, model_dic['pca_type_red'].transform(data), df['type'])
        data['type'] = wine_type(result['type_red'])
        data['quality'] = result['quality']
        df2 = new_dataframe(df, data)
        df2.to_csv(f'lib/data/winequality-flask.csv',index=False)
        return render_template('prediction.html', graphJson=graphJson, wine_result=wine_result)
    else:
        return render_template('prediction.html')


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
    TEMPLATES_AUTO_RELOAD = True