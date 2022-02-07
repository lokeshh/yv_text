import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import jsonpickle
from yv_verse import YvVerse
import ptp_utils

def read(filename):
    return jsonpickle.decode(open(filename).read())

def read_ptp():
  return yaml.safe_load(open('ptp.yaml', 'r').read())    

# cred = credentials.Certificate("/home/lokesh/Downloads/yv-api-5737d-firebase-adminsdk-qsosv-9c400a74ca.json")
cred = credentials.Certificate("/Users/lokesh/Downloads/yv-api-5737d-firebase-adminsdk-qsosv-80e7ff07e4.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yv-api-5737d.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
# vlm_core_ref = db.reference('yv/vlm')
# abs_ref = db.reference('yv/abs')
# count_ref = db.reference('yv/count')

def update_yv_core(yv_core_verses):
  yv_core_ref = db.reference('yv/yv_core')
  for i in yv_core_verses:
      yv_core_ref.child(str(i.book)).child(str(i.chapter)) \
          .update({i.verse: i.text})

def update_mk_core(mk_core_verses):
  mk_core_ref = db.reference('yv/mk_core')
  for i in mk_core_verses:
      mk_core_ref.child(str(i.book)).child(str(i.chapter)) \
          .update({i.verse: i.text})

def update_vlm(vlm_verses):
    for i in vlm_verses:
        vlm_core_ref.child(str(i.book)).child(str(i.chapter)) \
            .update({i.verse: i.text})

def update_abs(abs_verses):
    for i in abs_verses:
        abs_ref.child(str(i.book)).child(str(i.chapter)) \
            .update({i.verse: i.text})

def update_yv_ptp(book, chapter):
  yv_ptp_ref = db.reference('yv/yv_ptp')

  ptp_verses = ptp_utils.get_ptp_specific(book, chapter)
  
  yv_verses = ptp_utils.read_yv()
  yv_verses = [i for i in yv_verses if i.book == book and i.chapter == chapter]
  lines = []
  for i in yv_verses:
    for j in i.text:
      lines.append(f"<b>{j}</b>")
    if i.verse in ptp_verses:
      lines.append("\n")
      lines.extend(ptp_verses[i.verse])
      lines.append("\n\n")
  yv_ptp_ref.child(str(book)).update({str(chapter): lines})





# count_dict = {}
# for i in yv_core_verses:
#     if (i.book, i.chapter) not in count_dict:
#         count_dict[(i.book, i.chapter)] = i.verse
#     else:
#         count_dict[(i.book, i.chapter)] = max(count_dict[(i.book, i.chapter)], i.verse)

# for i in count_dict:
#     count_ref.child(str(i[0])).update({str(i[1]): count_dict[i]})

def update_db(book, chapter):
    yv_core_verses = read('yv_core.json')
    vlm_verses = read('vlm.json')
    abs_verses = read('abs.json')
    yv_core_verses = [i for i in yv_core_verses if i.book == book and i.chapter == chapter]
    vlm_verses = [i for i in vlm_verses if i.book == book and i.chapter == chapter]
    abs_verses = [i for i in abs_verses if i.book == book and i.chapter == chapter]
    # update_yv_core(yv_core_verses)
    # update_vlm(vlm_verses)
    update_abs(abs_verses)

    
# update_db(4, 25)

mk_core_verses = read('mk_core2.json')
filtered = [i for i in mk_core_verses if i.book == 6 and i.chapter > 120]
print(len(filtered))
update_mk_core(filtered)

# update_yv_core(read('yv_core.json'))

# update_yv_ptp(6, 40)
