from pathlib import Path
import re


SOURCE = Path(__file__).parent / "mk_raw.txt"
OUTPUT = Path(__file__).parent / "mk_sandhi.txt"

CONSONANTS = "kgṅcjñṭḍṇtdnpbmyrlvśṣsh"
VOWELS = "aāiīuūṛṝḷḹeo"
SANDHI_SPACE = re.compile(f"(?<=[{CONSONANTS}]) +(?=[{VOWELS}])")


def main():
    text = SOURCE.read_text(encoding="utf-8")
    OUTPUT.write_text(SANDHI_SPACE.sub("", text), encoding="utf-8")


if __name__ == "__main__":
    main()
