#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:54:31 2020

@author: josephwatkins
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

data = pd.read_csv('/Users/josephwatkins/Desktop/CS 450/WeatherPrediction/daily_high_temps_distinct.csv')

# clean the data using r or pandas to select out the max temperatures
# look up ways to make a neural network more accurate

def preprocess(df, target_location=0):
    ''' prepare the data for the machine learning algorithm '''
    X = df.drop(df.columns[target_location],axis=1)
    y = df[df.columns[target_location]]
    # split into testing and training sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, 
                                                        train_size=.7)
    # normalize the data
    scaler = StandardScaler()
    # Fit only to the training data
    scaler.fit(X_train)
    # Now apply the transformations to the data:
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

data2 = data.drop(data.columns[0], axis=1)
X_train, X_test, y_train, y_test = preprocess(data2, target_location = -1)

# run the neural network (multi layer perceptron)
nCols = len(X_train[0])
mlp = MLPRegressor(hidden_layer_sizes=(nCols,nCols,nCols),max_iter=700,
                    learning_rate='adaptive')
mlp.fit(X_train,y_train)
predictions = mlp.predict(X_test) # check how well it did
# Return the coefficient of determination R^2 of the prediction.
r2score = mlp.score(X_test, y_test)
print("R^2 score = {}".format(r2score))







