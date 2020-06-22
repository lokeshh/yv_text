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
mk = read('mk_core.json')

missing = 0
for x in mk:
    for y in yv:
        if fuzz.ratio(' '.join(x.text), ' '.join(y.text)) > 60:
            # print('match found')
            # print(x)
            # print(y)
            # print()
            break
    else:
        print('no match found for ', x)
        missing += 1

print('Total missing =', missing)