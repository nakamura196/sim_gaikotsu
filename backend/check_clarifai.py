import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
import requests
import shutil

files = glob.glob("data/clarifai/*.json")

result = {}
metadata = {}

oms = [
    "古いです",
    "昔からある",
    "何人もありません",
    "1",
    "二",
]

for file in files:

    with open(file) as f:
        try:
            df = json.load(f)

            id = file.split("/")[-1].split(".")[0]

            values = []

            for i in range(5):

                obj = df[i]
                label = obj["label"]

                if label in oms:
                    continue

                if label not in result:
                    result[label] = 0

                result[label] = result[label] + 1

                ############

                if label not in values:
                    values.append(label)

            metadata[id] = values
            
        except:
            print(file)

data = []
data.append(["label", "value"])

for key in result:
    data.append([key, result[key]])


with open('data/clarifais.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
    writer.writerows(data)  # 2次元配列も書き込める

fw2 = open("data/clarifais.json", 'w')
json.dump(metadata, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
