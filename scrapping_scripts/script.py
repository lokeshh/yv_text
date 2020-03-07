import requests
from yv_verse import YvVerse
import json
import jsonpickle
from multiprocessing import Pool
from bs4 import BeautifulSoup

from util import *

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

sitemap_link = 'https://www.wisdomlib.org/hinduism/book/yoga-vasistha-sanskrit/sitemap'
page = requests.get(sitemap_link)
soup = BeautifulSoup(page.text, 'html.parser')

verses = soup.find_all(class_ = 'py-1 py-md-0 il-cont cve')

yv_verses = []
p = Pool(20)

print(f"total verses = {len(verses)}")

# for i, v in list(enumerate(verses))[14000:14100:10]:
step = 20
for i in range(28000, 28260, step):
    try:
        print(f"{i} {verses[i].contents[1].a.contents[0]} to {verses[i+step-1].a.contents[0]}")
    except:
        print(f"{i} {verses[i].contents[1].a.contents[0]} to {verses[-1].a.contents[0]}")
    yv_verses.extend(p.map(extract_yv_verse, [str(k) for k in verses[i:i+step]]))

# breakpoint()
with open('28000-30000.json', 'w', encoding='utf-8') as f:
    f.write(jsonpickle.encode(yv_verses, max_depth=2))
