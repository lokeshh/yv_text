import jsonpickle
from yv_verse import YvVerse

def read_book(n):
    return jsonpickle.decode(open(f"book_{n}.json").read())

def save_book(n, yv_verses):
    with open('book_{n}', 'w', encoding='utf-8') as f:
        f.write(jsonpickle.encode(yv_verses, max_depth=2))

books = {}
for book_number in range(1, 8):
    books[book_number] = read_book(book_number)

breakpoint()