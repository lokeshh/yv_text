from bs4 import BeautifulSoup, NavigableString
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

def convert_to_dev(text):
    return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)


def read_soup():
    f = open('temp.html', 'r').read()
    return BeautifulSoup(f, 'html.parser')


def write_soup(soup):
    with open("temp-output2.html", "w", encoding='utf-8') as f2:
        f2.write(str(soup))

soup = read_soup()

def recurse(x):
    try:
        if type(x) == NavigableString:
            x.string.replace_with(convert_to_dev(x.string))
            # print(x.string)
            return
        for i in x.contents:
            recurse(i)
    except Exception as e:
        print(e)
        print('Failed')
        print(x)
        # print(x.contents)
        # breakpoint()
        print("\n\n\n")

recurse(soup)


# for i in soup.find_all('p'):
#     try:
#         i.string = convert_to_dev(i.string)
#     except:
#         try:
#             for j in i.contents:
#                 j.string = convert_to_dev(j.string)
#         except:
#             print(j)
#             print(j.string)
#             print('failed')
#             break

write_soup(soup)
breakpoint()
print('Complete')