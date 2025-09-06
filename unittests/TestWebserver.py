import unittest
import json
import os
from app import webserver

class TestWebserver(unittest.TestCase):
    def setUp(self):
        pass

    def test_states_mean(self): # test states_mean
        self.helper("states_mean")
    
    def test_state_mean(self): # test state_mean
        self.helper("state_mean")
    
    def test_best5(self): # test best5
        self.helper("best5")
    
    def test_worst5(self): # test worst5
        self.helper("worst5")

    def test_global_mean(self): # test global_mean
        self.helper("global_mean")

    def test_diff_from_mean(self): # test diff_from_mean
        self.helper("diff_from_mean")

    def test_state_diff_from_mean(self): # test state_diff_from_mean
        self.helper("state_diff_from_mean")

    def test_mean_by_category(self): # test mean_by_category
        self.helper("mean_by_category")

    def test_state_mean_by_category(self): # test state_mean_by_category
        self.helper("state_mean_by_category")

    # Helper method used for getting data from input file
    # answering the question and comparing the result with the data
    # from output file
    def helper(self, endpoint):
        output_dir = f"unittests/{endpoint}/output/"
        input_dir = f"unittests/{endpoint}/input/"

        for input_file in os.listdir(input_dir):
            
            idx = int(input_file.split('-')[1].split('.')[0])

            # Get data from input file
            with open(f"{input_dir}/in-{idx}.json", "r") as fin:
                data = json.load(fin)  # Load JSON data from the file object

                # Process question to get answer
                result = webserver.data_ingestor.answer_question(data, endpoint)

            # Get data from output file
            with open(f"{output_dir}/out-{idx}.json", "r") as fout:
                expected_result = json.load(fout)

            # Compare result of answer_question to the data from output file
            self.assertEqual(result, expected_result, f"Failed for input file: {input_file}")

if __name__ == "__main__":
    unittest.main()
