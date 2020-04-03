import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.ensemble import GradientBoostingRegressor


def analyze_predictions(predictions, targets, name):
    correct = 0
    for i in range(len(predictions)):
        if (targets[i] + 5) >= predictions[i] >= (targets[i] - 5):
            correct += 1
    print(f"{name} Correct: {correct}/{len(predictions)}    {correct/len(predictions) * 100:.2f}%")


def main():
    data = pd.read_csv("daily_high_temps_distinct.csv")
    data = data.drop(["TIMESTAMP", "RECORD"], axis=1)

    target_name = "AirTF_Avg"
    targets = pd.DataFrame.to_numpy(data.get(target_name))
    data = pd.DataFrame.to_numpy(data.drop(target_name, axis=1))

    data = normalize(data)

    train_size = int(np.shape(data)[0] / 100 * 70)

    data_train, data_test, targets_train, targets_test = train_test_split(data, targets,
                                                                          train_size=train_size)
    classifier = GradientBoostingRegressor(n_estimators=100)
    classifier.fit(data_train, targets_train)

    predictions = classifier.predict(data_test)

    analyze_predictions(predictions, targets_test, "GradientBoostingRegressor")

if __name__ == "__main__":
    # execute only if run as a script
    main()
