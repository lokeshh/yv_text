import re
from yv_verse import YvVerse
from os import listdir
from os.path import isfile, join
import jsonpickle

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

# mypath = 'wiki_yv'
# file_names = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])

# def replace_dev_nums(file_txt):
#     replace_dict = {}
#     dev_nums = '०१२३४५६७८९'
#     for i in range(10):
#         file_txt = file_txt.replace(dev_nums[i], str(i))
#     return file_txt

# mismatches = 0
# for file_name in file_names[:10]:
#     book, chapter = map(int, re.split('[_\.]', file_name)[:2])
#     file_txt = open('wiki_yv/' + file_name).read()
#     file_txt = replace_dev_nums(file_txt)
#     verses = re.split('\d+', file_txt)
#     verses = [i for i in verses if i not in ['\n', '', ' ॥', ' ।।']]
#     nums = re.split('\D+', file_txt)
#     nums = list(map(int, [i for i in nums if i != '']))

#     # print(book, chapter, len(verses), max(nums))
#     if len(verses) - 1 != max(nums):
#         print(book, chapter, len(verses), max(nums))
#         mismatches += 1
#         # breakpoint()

# print(mismatches)

def read_complete_book():
    return jsonpickle.decode(open(f"yv_core.json").read())

a = set()
verses = read_complete_book()
verses = [i for i in verses if i.book == 6]
for i in verses:
    for j in verses:
        if (i.book, i.chapter, i.verse) == (j.book, j.chapter, j.verse) and i.book <= 6:
            if i.text < j.text:
                print(i.book, i.chapter, i.verse, j.verse)
                print(i.text)
                print(j.text)

import xmltodict
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

def convert_to_dev(text):
    return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)

# mk_text = xmltodict.parse(open('mokshopaya.xml').read())

# book_1 = mk_text['TEI']['text']['body']['div'][1]['div']

# verses = []
# for chapter in book_1:
#     for verse in chapter['lg']:
#         print(verse)
#         yv_verse = YvVerse(*map(int, verse['@xml:id'].split('_')[1].split('.')))
#         text = []
#         for i in verse['l']:
#             text.append(transliterate(i, sanscript.IAST, sanscript.DEVANAGARI))
#         yv_verse.set_text(text)
#         verses.append(yv_verse)

import xml.etree.ElementTree as ET
tree = ET.parse('mokshopaya.xml')
root = tree.getroot()


# import lxml.etree as etree

# etree.parse("mokshopaya.xml").write("good.xml", encoding="utf-8")

import xml.etree.ElementTree as ET
tree = ET.parse('mokshopaya.xml')
root = tree.getroot()

tag_prefix = '{http://www.tei-c.org/ns/1.0}'
id_attrib = '{http://www.w3.org/XML/1998/namespace}id'
verses = []
buffer = []
for book in root[1][0]:
    for chapter in book:
        for node in chapter:
            if node.tag == tag_prefix + 'p':
                print(node.text)
                buffer.append(convert_to_dev(node.text))
            elif node.tag == tag_prefix + 'lg':
                yv_verse = YvVerse(*map(int, node.attrib[id_attrib].split('_')[1].split('.')))
                for l in node:
                    buffer.append(convert_to_dev(l.text))
                yv_verse.set_text(buffer)
                buffer = []
                verses.append(yv_verse)