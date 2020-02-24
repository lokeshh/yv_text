import jsonpickle
from yv_verse import YvVerse
from bs4 import BeautifulSoup
import re

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2, ensure_ascii=False)

def read_book(n):
    return jsonpickle.decode(open(f"book_{n}.json").read())

def save_book(n, yv_verses):
    with open(f"book_{n}.json", 'w', encoding='utf-8') as f:
        f.write(jsonpickle.encode(yv_verses, max_depth=3))

books = {}
complete_book = []
for book_number in range(1, 8):
    books[book_number] = read_book(book_number)
    complete_book.extend(books[book_number])

# def clean_text(yv_verse):
#     text = yv_verse.text
#     clean_text = []
#     for t in re.split('\[|\'|\]|\\\\n|, ', text):
#         if t in ['', '<br/>']:
#             continue
#         else:
#             clean_text.append(t.strip())
#     yv_verse.text = clean_text

def generate_complete(complete_book):
    complete_text = []
    for v in complete_book:
        complete_text.append(f"{v.book}.{v.chapter}.{v.verse}")
        complete_text.extend(v.text)
        complete_text.append("\n")
    return "\n".join(complete_text)


# with open('complete.txt', 'w') as f:
#     f.write(generate_complete(complete_book))

breakpoint()