#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib
import numpy as np
from joypy import joyplot
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import (KNeighborsClassifier,
                               NeighborhoodComponentsAnalysis)


# In[2]:


# setting up the path to read the datafiles
root = './data/*final.csv'
files = glob.glob(root)

def read_csv(files):
    for file in files:
        df = pd.read_csv(file)
    return df

def dataset_split(X,y):
#divide the data into training and testing set 
    X_train, X_test,y_train,y_test=train_test_split(X,y, random_state=42)
    return X_train, X_test,y_train,y_test

#Creating the linear regression model and fitting the data to it
def multilinear_regression(X,y):
    X_train,X_test,y_train,y_test = dataset_split(X,y)
    RG=make_pipeline(StandardScaler(),LinearRegression())
    regression = RG.fit(X_train,y_train)
    y_predict = regression.predict(X_test)
        # The coefficients
    print('Coefficients:')
    for x,cf in enumerate(regression[1].coef_):
        print(f"{X.columns[x]} = {cf}")
    # The intercept
    print('Intercept: %.2f' 
         % regression[1].intercept_)
    # The mean squared error
    print('Mean squared error: %.2f'
          % mean_squared_error(y_test, y_predict))
    # The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f'
          % r2_score(y_test, y_predict))
    if r2_score(y_test,y_predict) < 0.7 and mean_squared_error(y_test, y_predict) < 0.7:
        print('the dataset is NOT well represented by a linear model')
    return regression


# # Principal Component Analysis
def make_pca(n_components=None):
        pca = make_pipeline(StandardScaler(),
                        PCA(n_components=n_components, random_state=42))
        return pca


# # Dimension Reduction with PCA and Classification with kNN
def kNN_classification(X,y,n_neighbors,n_components):
    X_train,X_test,y_train,y_test = dataset_split(X,y)
    # Use a nearest neighbor classifier to evaluate the methods
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    pca = make_pca(n_components).fit(X_train,y_train)
    # Fit a nearest neighbor classifier on the embedded training set
    knn.fit(pca.transform(X_train), y_train)
    return knn, pca


def ML_wine_quality(files, wine_type, column_target):
    df = read_csv(files)
    df_wine = pd.get_dummies(df, columns=['type'])
    if wine_type != 'all':
        df_wine = df_wine[df_wine[f'type_{wine_type}'] == 1]
        
    type_column = list(df_wine.filter(regex='type_').columns)
    df_wine = df_wine.drop(columns=type_column[1])
    if column_target == 'type':
        column_target = [type_column[0]]
        column_target.extend(['quality'])

    else:
        column_target = [column_target]
        column_target.extend([type_column[0]])
    
    # setting up the data for quality evaluation
    X = df_wine.drop(columns=column_target)
    y = df_wine[column_target[0]]

    # find the optimal number of components
    matplotlib.rc_file_defaults()
    n_components = 4
    
    #dimension reduction and classification 
    n_neighbors = 3
    knn, pca = kNN_classification(X,y,n_neighbors,n_components)
    return knn,pca


data = pd.DataFrame.from_dict({'alcohol': [20],
 'chlorides':[.5],
 'citric_acid': [2],
 'fixed_acidity': [30],
 'free_sulfur_dioxide': [0.5],
 'total_sulfur_dioxide':[1.0],
 'density':[1.1],
 'pH':[3],
 'residual_sugar': [0.3],
 'sulphates':[0.2],
 'volatile_acidity':[5]}, orient='columns')

# predict the wine quality
def wine_quality(prediction):
    if prediction < 5 :
        quality = 'Poor Quality '
    elif prediction > 7:
        quality = 'Good Quality '
    else:
        quality = 'Average Quality '
    return quality

# predict the wine type
def wine_type(prediction):
    if prediction == 0:
        wtype='white'
    else:
        wtype='red'
    return wtype


def ML_predictions(files, data):
    t_knn,t_pca = ML_wine_quality(files,'all', 'type')
    wtype = wine_type(t_knn.predict(t_pca.transform(data)))
    knn,pca = ML_wine_quality(files,wtype,'quality')
    qual = wine_quality(knn.predict(pca.transform(data)))
    return (wtype.capitalize(), qual.capitalize())



wtype, qual = ML_predictions(files,data)
print(wtype,' Wine of ', qual)

