"""
Data Ingestor Module

This module contains a class `DataIngestor` that represents a data handler. 
It provides methods to read CSV data and answer questions based on the data.
"""
import pandas as pd

class DataIngestor:
    """Class representing a data handler that gets a question and returns an answer"""

    def __init__(self, csv_path: str):
        # Read csv from csv_path
        self.csv_data = pd.read_csv(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of '
            'moderate-intensity aerobic physical activity or '
            '75 minutes a week of '
            'vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of '
            'moderate-intensity aerobic physical activity or '
            '75 minutes a week of '
            'vigorous-intensity aerobic physical activity and engage in '
            'muscle-strengthening activities '
            'on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of '
            'moderate-intensity aerobic physical activity or '
            '150 minutes a week of vigorous-intensity aerobic physical '
            'activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities '
            'on 2 or more days a week',
        ]

    # Get all table lines from the file that
    # satisfy the given question
    def answer_question(self, data, question_type):
        """Method that gets question and answes it"""

        # Extract question from json
        question = data['question']

        # Filter table based on the question
        table = self.csv_data[self.csv_data['Question'] == question]

        results = {}

        # Go through each type of endpoint
        # For each one I get the mean based on the criteria
        # and then I return the result into a dictionary
        # This dictionary will represent the data that I will return
        # when I try to get a result for a certain job_id
        if question_type == "states_mean":
            mean = table.groupby("LocationDesc")["Data_Value"].mean()
            results = dict(sorted(mean.items(), key=lambda item: item[1]))

        elif question_type == "state_mean":
            state = data['state']
            mean = table.groupby("LocationDesc")["Data_Value"].mean()
            results = {k: v for k, v in
                       sorted(mean.items(), key=lambda item: item[1]) if k == state}

        elif question_type == "best5":
            mean = table.groupby("LocationDesc")["Data_Value"].mean()
            results = dict(mean.sort_values(ascending=question
                                            in self.questions_best_is_min).head(5))

        elif question_type == "worst5":
            mean = table.groupby("LocationDesc")["Data_Value"].mean()
            results = dict(mean.sort_values(ascending=question
                                            not in self.questions_best_is_min).head(5))

        elif question_type == "global_mean":
            mean = table["Data_Value"].mean()
            results = {'global_mean': mean}

        elif question_type == "diff_from_mean":
            states_mean = table.groupby("LocationDesc")["Data_Value"].mean()
            global_mean = table["Data_Value"].mean()
            results = {k: global_mean - v for k, v in
                       sorted(states_mean.items(), key=lambda item: item[1])}

        elif question_type == "state_diff_from_mean":
            state = data['state']
            states_mean = table.groupby("LocationDesc")["Data_Value"].mean()
            global_mean = table["Data_Value"].mean()
            results = {k: global_mean - v for k, v in
                       sorted(states_mean.items(), key=lambda item: item[1]) if k == state}

        elif question_type == "mean_by_category":
            mean = table.groupby(['LocationDesc', 'Stratification1', 'StratificationCategory1']) \
                    ['Data_Value'].mean().reset_index()

            for _, row in mean.iterrows():
                location = row['LocationDesc']
                info = row['Stratification1']
                category = row['StratificationCategory1']
                value = row['Data_Value']
                key = f"('{location}', '{category}', '{info}')"
                results[key] = value

        else:
            temp_dict = {}
            state = data['state']
            mean = table.groupby(['LocationDesc', 'Stratification1', 'StratificationCategory1']) \
                    ['Data_Value'].mean().reset_index()
            for _, row in mean.iterrows():
                location = row['LocationDesc']
                if location == state:
                    info = row['Stratification1']
                    category = row['StratificationCategory1']
                    value = row['Data_Value']
                    key = f"('{category}', '{info}')"
                    temp_dict[key] = value
            results[state] = temp_dict

        return results
