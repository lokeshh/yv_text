import yaml
import jsonpickle
from yv_verse import YvVerse
import markdown

def read_ptp():
  return yaml.safe_load(open('ptp.yaml', 'r').read())

def read_yv():
  return jsonpickle.decode(open(f"yv_core.json").read())

def get_ptp_specific(book, chapter):
  ptp_verses = read_ptp()
  verses = []
  for i in ptp_verses:
    if i['book'] == book:
      for j in i['content']:
        if j['chapter'] == chapter:
          verses = j['content']
          break
      break
  ptp_verses = {}
  for i in verses:
    ptp_verses[i['verse']] = i['content']
  return ptp_verses

def bold(lines):
  lines[0] = "<b>" + lines[0]
  lines[-1] = lines[-1] + "</b>"
  return lines

def generate_chapter_md_lines(book, chapter):
  yv_verses = read_yv()
  yv_verses = [i for i in yv_verses if i.book == book and i.chapter == chapter]
  ptp_verses = get_ptp_specific(book, chapter)
  lines = [f"{book}.{chapter}"]
  for i in yv_verses:
    lines.extend(bold(i.text))
    if i.verse in ptp_verses:
      lines.append("\n")
      lines.extend(ptp_verses[i.verse])
      lines.append("\n\n")
  return lines

def write_to_md(book, chapter):
  lines = generate_chapter_md_lines(book, chapter)
  with open('test.md', 'w') as f:
    f.write("\n".join(lines))

def add_chapter(book, chapter, verses):
  ptp_verses = read_ptp()
  chapter_data = {'chapter': chapter, 'content': []}
  for i in range(1, verses + 1):
    chapter_data['content'].append({'verse': i, 'content': [None]})
  ptp_verses[0]['content'].append(chapter_data)
  yaml.dump(ptp_verses, open('ptp_test.yaml', 'w'), allow_unicode=True)

# add_chapter(6, 41, 59)

# ptp_verses = read_ptp()

lines = [
  *generate_chapter_md_lines(6, 40),
  *generate_chapter_md_lines(6, 41)
]
html_lines = []
for line in lines:
  html_lines.append(line + "<br />")
md_text = "\n".join(html_lines)
with open('6(40-41).html', 'w') as f:
  f.write(md_text)