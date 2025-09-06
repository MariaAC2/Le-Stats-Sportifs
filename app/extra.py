"""
Extra Module

This module contains the 'Job' class that handles the execution of
the task with the given requirements.

It also contains some functions that handle the results folder,
by creating the path using a job id ('create_path'), writing the result into the
file with the given job id ('post_result') and reading from the file with 
the given job id and returning the result ('get_result')
"""
import os
import json

FOLDER_PATH = "results"

class Job:
    """Class that handles the execution of a task"""
    def __init__(self, job_type, job_id, data, data_ingestor):
        """Method that initiates the Job class"""
        self.job_id = job_id
        self.status = "running"
        self.type = job_type
        self.data = data
        self.data_ingestor = data_ingestor

    # Get the answer from the data digestor and return it
    def execute(self):
        """Method that executes the given job"""
        results = self.data_ingestor.answer_question(self.data, self.type)
        return results

# Create the file path for getting and posting
# the result in the results folder
def create_path(job_id):
    """Function that creates path"""
    file_name = job_id + ".json"
    file_path = os.path.join(FOLDER_PATH, file_name)

    return file_path

# This writes the result after the execution of the
# task in a file with path "results/job_id_{job_id}"
def post_result(job_id, result):
    """Function that writes result into the file"""
    file_path = create_path(job_id)
    # Check if the folder exists, if not, create it
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    # Check if the file exists, if not, create it
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding='utf-8') as file:
            file.close()

    # Write into the file
    data = json.dumps(result)
    with open(file_path, "a", encoding='utf-8') as file:
        file.write(data)

# This function returns an empty dict if the job is not done
# Otherwise, it returns a dict representing the result
def get_result(job_id):
    """Function that reads result from file"""
    file_path = create_path(job_id)

    result = {}
    # Check if the file exists
    if os.path.exists(file_path):

        # Read from the file
        with open(file_path, "r", encoding='utf-8') as file:
            data = file.read()

            # If data exists, return the result
            if data:
                result = json.loads(data)

            # There isn't a case where the file exists
            # but there is no data in file
            else:
                pass

    # If not, return the empty result
    return result
