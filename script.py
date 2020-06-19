import re
from yv_verse import YvVerse
from os import listdir
from os.path import isfile, join
import jsonpickle

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

mypath = 'wiki_yv'
file_names = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])

def replace_dev_nums(file_txt):
    replace_dict = {}
    dev_nums = '०१२३४५६७८९'
    for i in range(10):
        file_txt = file_txt.replace(dev_nums[i], str(i))
    return file_txt

mismatches = 0
for file_name in file_names[:10]:
    book, chapter = map(int, re.split('[_\.]', file_name)[:2])
    file_txt = open('wiki_yv/' + file_name).read()
    file_txt = replace_dev_nums(file_txt)
    verses = re.split('\d+', file_txt)
    verses = [i for i in verses if i not in ['\n', '', ' ॥', ' ।।']]
    nums = re.split('\D+', file_txt)
    nums = list(map(int, [i for i in nums if i != '']))

    # print(book, chapter, len(verses), max(nums))
    if len(verses) - 1 != max(nums):
        print(book, chapter, len(verses), max(nums))
        mismatches += 1
        # breakpoint()

# print(mismatches)

a = set()
verses = read_complete_book()
for i in verses:
    for j in verses:
        if (i.book, i.chapter, i.verse) == (j.book, j.chapter, j.verse) and i.book <= 6:
            if i.text < j.text:
                print(i.book, i.chapter, i.verse, j.verse)
                print(i.text)
                print(j.text)