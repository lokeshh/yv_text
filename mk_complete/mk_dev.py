from pathlib import Path
import re

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


SOURCE = Path(__file__).parent / "mk_sandhi.txt"
OUTPUT = Path(__file__).parent / "mk_dev.txt"


def main():
    text = SOURCE.read_text(encoding="utf-8")
    text = re.sub(r"\.\.|[.,]", lambda match: {"..": "॥", ".": "।", ",": "."}[match.group()], text)
    text = text.translate(str.maketrans({"ẖ": "ᳵ", "ḫ": "ᳶ"}))
    devanagari = transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)
    OUTPUT.write_text(devanagari, encoding="utf-8")


if __name__ == "__main__":
    main()
