import json

class YvVerse:
    def __init__(self, book, chapter, verse):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.text = None

    def set_text(self, text):
        self.text = text

    def __repr__(self):
        return f"{self.book}.{self.chapter}.{self.verse} {self.text}"
