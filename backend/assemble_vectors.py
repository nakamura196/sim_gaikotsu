import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
import requests
import shutil

files = glob.glob("output/image_vectors/*.npy")

features = []

for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1))

    file = files[i]
    a = numpy.load(file)
    features.append(a)

numpy.save('data/features.npy', features)

with open('data/features_list.json', 'w') as outfile:
    json.dump(files, outfile, ensure_ascii=False,
              sort_keys=True, separators=(',', ': '))

print("画像総数：")
print(len(features))

