"""
    process_data.py

    Averages dated numeric information from a CSV file.
    It expects the headers to at least include TIMESTAMP for processing.

    Author: Michael Hegerhorst
"""
import sys

import pandas as pd


class Date:
    def __init__(self, year, month, day):
        self.month = month
        self.day = day
        self.year = year

    def eq_ni_year(self, other):
        if self.day != other.day:
            return False
        if self.month != other.month:
            return False
        return True

    def __eq__(self, other):
        if self.day != other.day:
            return False
        if self.month != other.month:
            return False
        if self.year != other.year:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        str_month = self.month
        if self.month < 10:
            str_month = "0" + str(self.month)
        str_day = self.day
        if self.day < 10:
            str_day = "0" + str(self.day)

        return f"{self.year}-{str_month}-{str_day}"

    def __repr__(self):
        return self.__str__()


def parse_date(date_string):
    date_string = date_string.split(" ")[0]
    month, day, year = date_string.split("/")
    return Date(int(year), int(month), int(day))


def process_date_data(date_data):
    columns = list(date_data[0].keys())
    num_dates = len(date_data)
    date = str(parse_date(date_data[0].values[0]))
    avgs = []

    min_columns = []
    mins = []

    max_columns = []
    maxes = []

    for i in range(1, len(columns)):
        min_columns.append("min_" + columns[i])
        max_columns.append("max_" + columns[i])

    for col in range(1, len(columns)):
        minimum = sys.maxsize
        maximum = -sys.maxsize - 1
        average = 0
        for row in range(0, num_dates):
            value = date_data[row][col]
            average += value
            if value < minimum:
                minimum = value
            elif value > maximum:
                maximum = value
        average /= num_dates
        mins.append(minimum)
        maxes.append(maximum)
        avgs.append(average)

    columns = columns[1:] + min_columns + max_columns
    data = avgs + mins + maxes

    return pd.Series(index=columns, data=data, name=date)


def main():
    name = "CR6Series_TenMin"
    file_extension = ".csv"
    data = pd.read_csv("processable_" + name + file_extension)
    data = data.drop_duplicates()
    try:
        data = data.drop("RECORD", axis=1)
    except Exception:
        pass


    print("Sorting:")
    num_rows = data.shape[0] - 1
    current_date = Date(0, 0, 0)
    dates = []
    dates_i = -1
    for index, row in data.iterrows():
        print(f"{index}/{num_rows}")
        date = parse_date(row.TIMESTAMP)
        if not date.eq_ni_year(current_date):
            current_date = date
            dates_i += 1
            dates.append([])
        dates[dates_i].append(row)

    print("\nProcessing:")
    processed_data = pd.DataFrame()
    num_dates = len(dates)
    for i in range(0, num_dates):
        print(f"{i + 1}/{num_dates}")
        row = pd.DataFrame([process_date_data(dates[i])])
        processed_data = processed_data.append(row)
    print(processed_data)

    try:
        pd.DataFrame.to_csv(processed_data, "processed_" + name + file_extension)
    except Exception as e:
        print("\nUnable to write to file. Make sure it's not currently in use.")
        print(e)

    return


if __name__ == "__main__":
    # execute only if run as a script
    main()
