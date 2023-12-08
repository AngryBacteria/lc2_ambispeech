import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(dir_path, "lc2_data.json")

with open(json_file_path, "r", encoding="utf-8") as file:
    nlp_data = json.load(file)
