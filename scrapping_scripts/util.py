from bs4 import BeautifulSoup
import requests
from yv_verse import *

def extract_yv_verse(v):
    v = BeautifulSoup(v, 'html.parser')
    v = v.contents[0]
    book, chapter, verse = map(int, v.contents[1].a.contents[0].split()[1].split('.'))
    v_page = requests.get('https://www.wisdomlib.org' + v.contents[1].a['href'])
    soup2 = BeautifulSoup(v_page.text, 'html.parser')
    verse_object = YvVerse(book, chapter, verse)
    try:
        verse_object.set_text(str(soup2.find(class_='text-sanskrit').p.contents))
    except:
        verse_object.set_text('TODO')
    return verse_object