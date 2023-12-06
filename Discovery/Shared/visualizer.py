import json
import pandas as pd
import matplotlib as plt
import tqdm

filename = 'logs.jsonl'

with open(filename, "r") as file:
    data = json.load(file)

print(data)