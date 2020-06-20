import xml.etree.ElementTree as ET
tree = ET.parse('mokshopaya.xml')
root = tree.getroot()
import re
from yv_verse import YvVerse
from os import listdir
from os.path import isfile, join
import jsonpickle
import xmltodict
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

def convert_to_dev(text):
    return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)

def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(jsonpickle.encode(data, max_depth=3)) 

tag_prefix = '{http://www.tei-c.org/ns/1.0}'
id_attrib = '{http://www.w3.org/XML/1998/namespace}id'
verses = []
buffer = []
try:
    for book in root[1][0]:
        for chapter in book:
            for node in chapter:
                if node.tag == tag_prefix + 'p':
                    if id_attrib not in node.attrib:
                        if not (len(node.text) >= 6 and node.text[-6:] == 'sargaḥ'):
                            print(node.text)
                            buffer.append(convert_to_dev(node.text))
                    else:
                        yv_verse = YvVerse(*map(int, node.attrib[id_attrib].split('_')[1].split('.')))
                        buffer.append(convert_to_dev(node.text))
                        yv_verse.set_text(buffer)
                        buffer = []
                        verses.append(yv_verse)
                elif node.tag == tag_prefix + 'lg':
                    yv_verse = YvVerse(*map(int, node.attrib[id_attrib].split('_')[1].split('.')))
                    for l in node:
                        buffer.append(convert_to_dev(l.text))
                    yv_verse.set_text(buffer)
                    buffer = []
                    verses.append(yv_verse)
except:
    breakpoint()

print('completed')
save(verses, 'mk_core.json')

breakpoint()