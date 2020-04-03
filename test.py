import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score

data = pd.read_csv(
    r"https://raw.githubusercontent.com/joeymwatkins/WeatherPrediction/master/daily_high_temps_distinct.csv")
data_ready = data.drop(columns='TIMESTAMP', axis=1)
data_ready = pd.DataFrame(data_ready)

scaled_data = pd.DataFrame(preprocessing.scale(data_ready[data_ready.columns[:-1]]))
prediction_data = np.array(data_ready[data_ready.columns[-1]])

train_data, test_data, train_target, test_target = train_test_split(
    scaled_data, prediction_data, test_size=0.3, train_size=0.7)

nCols = len(scaled_data.columns)

gbc = GradientBoostingRegressor(n_estimators=1500, max_depth=8,
                                min_samples_split=3, min_samples_leaf=6,
                                max_features=4)

gbc.fit(train_data, train_target)

predictions = gbc.predict(test_data)

r2 = r2_score(test_target, predictions)

# print("Our R-squared score returned: ", r2)
# print("This Score is roughly within", 61-61*r2,
#      "degrees of the average temperature of 61 degrees.")
# print("Target vs Predicted: ", test_target, predictions)

# def print_results(predictions,test_target):

print("Pred.     Targ.   Dif.")
for i in range(len(predictions)):
    print(f"{predictions[i]:.2f}     {test_target[i]:.2f}   {predictions[i] - test_target[i]:.2f}")
