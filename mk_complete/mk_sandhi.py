from pathlib import Path
import re


SOURCE = Path(__file__).parent / "mk_raw.txt"
OUTPUT = Path(__file__).parent / "mk_sandhi.txt"

CONSONANTS = "kgṅcjñṭḍṇtdnpbmyrlvśṣsh"
VOWELS = "aāiīuūṛṝḷḹeo'ṃḥẖḫ"
SANDHI_SPACE = re.compile(
    f"(?<=[{CONSONANTS}{VOWELS}]) +(?=[{CONSONANTS}{VOWELS}])"
)


def shift_separators_after_nearest_vowel(text, separator_char):
    result = []
    for line in text.splitlines(keepends=True):
        parts = line.split(separator_char)
        plain_text = "".join(parts)
        separator_positions = []
        position = 0
        for part in parts[:-1]:
            position += len(part)
            separator_positions.append(position)

        insertions = set()
        for position in separator_positions:
            vowel_position = next(
                (
                    index
                    for index in range(position - 1, -1, -1)
                    if plain_text[index] in VOWELS
                ),
                None,
            )
            target = vowel_position + 1 if vowel_position is not None else position
            insertions.add(target)

        for index in range(len(plain_text) + 1):
            if index in insertions:
                result.append(separator_char)
            if index < len(plain_text):
                result.append(plain_text[index])

    return "".join(result)


def main():
    text = SOURCE.read_text(encoding="utf-8")
    separator_char = "𑇈"
    text = SANDHI_SPACE.sub(separator_char, text)
    text = shift_separators_after_nearest_vowel(text, separator_char)
    OUTPUT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
