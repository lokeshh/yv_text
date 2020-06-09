import jsonpickle
from yv_verse import YvVerse
from bs4 import BeautifulSoup
import re

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


# with tbl.batch_writer(overwrite_by_pkeys=['id']) as batch:
#     for v in books[7]:
#         batch.put_item(Item={'id': get_id(v), 'text': v.text})

# count_tbl = dynamo.Table('count')
# with count_tbl.batch_writer(overwrite_by_pkeys=['id']) as batch:
#     for x in count_dict:
#         batch.put_item(Item={'id': x, 'value': count_dict[x]})

vlm = read('vlm.json')
abs = read('abs.json')

for i in vlm:
    if i.book == 3 and i.chapter in [109, 110]:
        i.text = [""]
        abs.append(i)

save(abs, 'abs.json')

abs = read('abs.json')
abs = [i for i in abs if i.chapter > 108]
for v in abs:
    comm_table.put_item(Item = {'id': 10000000 + get_id(v), 'text': v.text, 'author': 'abs'})
