import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import jsonpickle
from yv_verse import YvVerse

def read(filename):
    return jsonpickle.decode(open(filename).read())

cred = credentials.Certificate("/home/lokesh/Downloads/yv-api-5737d-firebase-adminsdk-qsosv-9c400a74ca.json")


firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yv-api-5737d.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
yv_core_ref = db.reference('yv/yv_core')
mk_core_ref = db.reference('yv/mk_core')
vlm_core_ref = db.reference('yv/vlm')
abs_ref = db.reference('yv/abs')
count_ref = db.reference('yv/count')

def update_yv_core(yv_core_verses):
    for i in yv_core_verses:
        yv_core_ref.child(str(i.book)).child(str(i.chapter)) \
            .update({i.verse: i.text})

def update_mk_core(mk_core_verses):
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

# mk_core_verses = read('mk_core2.json')
# update_mk_core(mk_core_verses)

update_yv_core(read('yv_core.json'))
