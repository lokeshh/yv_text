import jsonpickle
from yv_verse import YvVerse
import re

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

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

txt = generate_complete(mk)
with open('mokshopaya.md', 'w') as f:
    f.write(txt)