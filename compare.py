import jsonpickle
from yv_verse import YvVerse
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz


jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
import boto3

dynamo = boto3.resource("dynamodb")
# tbl = dynamo.Table("users")
verse_table = dynamo.Table('verse')
count_table = dynamo.Table('count')
comm_table = dynamo.Table('commentary')

def read_complete_book():
    return jsonpickle.decode(open(f"complete_yv_core.json").read())

def read(filename):
    return jsonpickle.decode(open(filename).read())

def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(jsonpickle.encode(data, max_depth=3))     

def generate_complete(complete_book):
    complete_text = []
    for v in complete_book:
        complete_text.append(f"{v.book}.{v.chapter}.{v.verse}")
        complete_text.extend(v.text)
        complete_text.append("\n")
    return "\n".join(complete_text)

def get_id(v):
    return int(v.book * 1e6 + v.chapter * 1e3 + v.verse)

yv = read('yv_core.json')
mk = read('mk_core2.json')

scores = []
for x in mk:
    max_score = 0
    for y in yv:
        s = fuzz.ratio(' '.join(x.text), ' '.join(y.text))
        max_score = max(s, max_score)
            # print('match found')
            # print(x)
            # print(y)
            # print()
        if max_score > 80:
            break
    scores.append((x, max_score))

    # if len(scores) % 1000 == 0:
    #     scores.sort(key = lambda x: x[1])
    #     breakpoint()

breakpoint()


for i in scores:
    if i[0].book == 3 and i[0].chapter == 130:
        print(i[0].verse, i[1])


unique_chapters = {}
for i in scores[:500]:
    unique_chapters[(i[0].book, i[0].chapter)] = unique_chapters.get((i[0].book, i[0].chapter), 0) + 1

