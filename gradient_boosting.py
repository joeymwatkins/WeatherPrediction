import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score


def analyze_predictions(predictions, targets, name):
    correct = 0
    for i in range(len(predictions)):
        if (targets[i] + 5) >= predictions[i] >= (targets[i] - 5):
            correct += 1
    print(f"{name} Correct: {correct}/{len(predictions)}    {correct / len(predictions) * 100:.2f}%")


def print_results(predictions, targets):
    print("Pred.     Targ.   Dif.")
    for i in range(len(predictions)):
        diff = predictions[i] - targets[i]
        print(f"{predictions[i]:.2f}     {diff:.2f}")


def get_within(predictions, targets, degrees):
    num_within = 0
    for i in range(len(predictions)):
        if (targets[i] - degrees) <= predictions[i] <= (targets[i] + degrees):
            num_within += 1
    print(f"Within {degrees} degrees: {num_within}")


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
    classifier = GradientBoostingRegressor(n_estimators=100, max_depth=8, min_samples_split=3, min_samples_leaf=6,
                                           max_features=4)
    classifier.fit(data_train, targets_train)

    predictions = classifier.predict(data_test)

    analyze_predictions(predictions, targets_test, "GradientBoostingRegressor")

    r2 = r2_score(targets_test, predictions)

    print(f"Avg. Difference: {61 - 61 * r2}")

    print(f"R2: {r2}")

    print_results(predictions, targets_test)
    get_within(predictions, targets, 5)


if __name__ == "__main__":
    # execute only if run as a script
    main()
