import time
from flask import Flask, render_template, request, jsonify  # 追加
from helper import *
from random import *
import urllib.request
import json
import numpy
from scipy import spatial
import os
from flask_cors import CORS
from annoy import AnnoyIndex
from nltk import ngrams
import random
import glob
import os
import codecs
import random
import numpy as np
import collections
# ソースコード
import copy

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)

app.config['JSON_AS_ASCII'] = False  # 日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False  # ソートをそのまま

MODEL_PATH = 'classify_image_graph_def.pb'

start = time.time()

##################

path = "features.npy"
features2 = numpy.load(path)

t1 = time.time() - start
print("features2 = numpy.load(path):{0}".format(t1) + "[sec]")

##################

with open('data.json') as f:
    files = json.load(f)

t1 = time.time() - start
print("json.load(f):{0}".format(t1) + "[sec]")

##################

# data structures
file_index_to_file_name = {}
file_index_to_file_vector = {}

# config
dims = 2048
n_nearest_neighbors = 60
# trees = 10000
trees = 100
# infiles = glob.glob('image_vectors/*.npy')

# t0 = time.time() - start
# print("before build ann index:{0}".format(t0) + "[sec]")

# build ann index
t = AnnoyIndex(dims)

# t8 = time.time() - start
# print("after build ann index:{0}".format(t8) + "[sec]")

'''

for file_index, i in enumerate(infiles):
    file_vector = np.load(i)
    file_name = os.path.basename(i).split('.')[0]
    file_index_to_file_name[file_index] = file_name
    file_index_to_file_vector[file_index] = file_vector
    t.add_item(file_index, file_vector)

'''

for file_index in range(len(features2)):
    # print(file_index)
    file_vector = features2[file_index]
    if str(file_index) in files:
        file_name = files[str(file_index)]["id"].split("/")[-1]
        file_index_to_file_name[file_index] = file_name
        file_index_to_file_vector[file_index] = file_vector
        t.add_item(file_index, file_vector)

t1 = time.time() - start
print("enumerate(infiles):{0}".format(t1) + "[sec]")

t.build(trees)

t1 = time.time() - start
print("t.build(trees):{0}".format(t1) + "[sec]")

##################

metadata = {}
thumbs = {}
ids = {}

for id in files:

    file = files[id]

    thumbs[file["thumbnail"]] = file["index"]

    metadata_array = files[id]["metadata"]

    id2 = file["id"].split("/")[-1]
    ids[id2] = file["index"]

    for obj in metadata_array:
        label = obj["label"]
        value = obj["value"]

        if label not in metadata:
            metadata[label] = {}

        if value not in metadata[label]:
            metadata[label][value] = []

        if id not in metadata[label][value]:
            metadata[label][value].append(id)

metadata_summary = {}

for field in metadata:
    obj = metadata[field]

    metadata_summary[field] = {}

    for label in obj:
        metadata_summary[field][label] = len(obj[label])

    sorted_x = sorted(
        metadata_summary[field].items(), key=lambda kv: kv[1], reverse=True)
    metadata_summary[field] = collections.OrderedDict(sorted_x)

t1 = time.time() - start
print("END:{0}".format(t1) + "[sec]")

##################

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/asearch')
def api_asearch():

    # start = time.time()

    url = request.args.get('url', default=None, type=str)
    CANDIDATES = request.args.get('rows', default=40, type=int)

    CANDIDATES -= 1

    if url != None:

        if url in thumbs:
            query_feat = features2[thumbs[url]]
        else:

            query_img = "/tmp/tmp.jpg"
            urllib.request.urlretrieve(url, "{0}".format(query_img))

            with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

            print("... End of FastGFile")

            with tf.Session() as sess:
                pool3 = sess.graph.get_tensor_by_name('pool_3:0')

                image_data = tf.gfile.FastGFile(query_img, 'rb').read()
                pool3_features = sess.run(
                    pool3, {'DecodeJpeg/contents:0': image_data})
                query_feat = np.squeeze(pool3_features)

            print("... End of Session")

    else:
        return jsonify([])

    master_vector = query_feat

    # t1 = time.time() - start
    # print("入力画像の読み込み:{0}".format(t1) + "[sec]")

    nearest_neighbors = t.get_nns_by_vector(master_vector, n_nearest_neighbors)

    # t2 = time.time() - start
    # print("類似画像の抽出:{0}".format(t2) + "[sec]")


    data = []

    for j in nearest_neighbors:
        neighbor_file_name = file_index_to_file_name[j]
        neighbor_file_vector = file_index_to_file_vector[j]

        similarity = 1 - \
            spatial.distance.cosine(master_vector, neighbor_file_vector)
        rounded_similarity = int((similarity * 10000)) / 10000.0

        obj = files[str(ids[neighbor_file_name])]
        obj["score"] = rounded_similarity
        data.append(obj)

    return jsonify(data)


@app.route('/api/search')
def api_search():

    # start = time.time()

    url = request.args.get('url', default=None, type=str)
    CANDIDATES = request.args.get('rows', default=40, type=int)

    CANDIDATES -= 1

    if url != None:

        if url in thumbs:
            query_feat = features2[thumbs[url]]
        else:

            query_img = "/tmp/tmp.jpg"
            urllib.request.urlretrieve(url, "{0}".format(query_img))

            with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

            print("... End of FastGFile")

            with tf.Session() as sess:
                pool3 = sess.graph.get_tensor_by_name('pool_3:0')

                image_data = tf.gfile.FastGFile(query_img, 'rb').read()
                pool3_features = sess.run(
                    pool3, {'DecodeJpeg/contents:0': image_data})
                query_feat = np.squeeze(pool3_features)

            print("... End of Session")

    else:
        return jsonify([])

    # t1 = time.time() - start
    # print("入力画像の読み込み:{0}".format(t1) + "[sec]")

    sims = [(k, round(1 - spatial.distance.cosine(query_feat, v), 3))
            for k, v in enumerate(features2)]

    # t2 = time.time() - start
    # print("類似画像の抽出:{0}".format(t2) + "[sec]")

    data = []

    arr = sorted(sims, key=operator.itemgetter(1),
                 reverse=True)[:CANDIDATES + 1]
    for e in arr:
        index = e[0]

        # temp
        if str(index) not in files:
            continue

        obj = copy.copy(files[str(index)])
        obj["score"] = e[1]
        data.append(obj)

    # t3 = time.time() - start
    # print("必要画像の抽出:{0}".format(t3) + "[sec]")

    return jsonify(data)

@app.route('/api/msearch')
def api_msearch():

    where_metadata_label = request.args.get(
         'where_metadata_label', default=None, type=str)
    where_metadata_value = request.args.get(
        'where_metadata_value', default=None, type=str)
    rows = request.args.get('rows', default=40, type=int)

    metadata_arr = metadata[where_metadata_label][where_metadata_value]

    if rows > len(metadata_arr):
        rows = len(metadata_arr)

    indexes = random.sample(metadata_arr, rows)

    data = []

    for index in indexes:
        obj = files[str(index)]
        data.append(obj)

    return jsonify(data)

@app.route('/api/random')
def api_random():

    rows = request.args.get('rows', default=40, type=int)

    data = []

    import random
    indexes = random.sample(files.keys(), rows)

    for index in indexes:
        obj = files[str(index)]
        data.append(obj)

    return jsonify(data)


@app.route('/api/metadata')
def api_metadata():


    return jsonify(metadata_summary)


# おまじない
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
