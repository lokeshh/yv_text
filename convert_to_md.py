import jsonpickle
from yv_verse import YvVerse
import re

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

def read(filename):
    return jsonpickle.decode(open(filename).read())

def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(jsonpickle.encode(data, max_depth=3))     

def generate_md(data):
    md_text = []
    for v in data:
        md_text.append(f"{v.book}.{v.chapter}.{v.verse}")
        md_text.extend(v.text)
        md_text.append("\n")
    return "\n".join(md_text)


def get_id(v):
    return int(v.book * 1e6 + v.chapter * 1e3 + v.verse)

yv = read('yv_core.json')
mk = read('mk_core2.json')

for book in range(1, 7):
    for chapter in range(1,1000):
        chapter_data = [i for i in mk if i.book == book and i.chapter == chapter]
        if chapter_data == []:
            continue
        md_text = generate_md(chapter_data)
        with open(f"mk_md/{book}/{chapter}.md", 'w') as f:
            f.write(md_text)


# txt = generate_md(mk)
# with open('mokshopaya.md', 'w') as f:
#     f.write(txt)