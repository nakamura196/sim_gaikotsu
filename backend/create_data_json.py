import glob
import json
import urllib.request
import csv
from hashlib import md5

import shutil

with open('data/features_list.json') as f:
    df = json.load(f)

with open('data/base.json') as f:
    metadata = json.load(f)

with open('data/clarifais.json') as f:
    clarifais = json.load(f)

data = {}

for i in range(len(df)):
    id = df[i].split("/")[-1].split(".")[0]

    if id in metadata:
        obj = metadata[id]
        obj["index"] = i

        if id in clarifais:
            for yolo in clarifais[id]:
                obj["metadata"].append({
                    "label" : "機械タグ",
                    "value" : yolo
                })

        data[i] = obj

with open('data/data.json', 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))

print("画像総数：")
print(len(df))

print("メタデータ数：")
print(len(data))
