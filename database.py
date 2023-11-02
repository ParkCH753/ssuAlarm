import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os
import json
import traceback
from firebase_admin import firestore

load_dotenv()

#firebase db 인증 및 앱 초기화
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred,
                              {'databaseURL' : os.environ.get('DATABASE_URL')}
)

"""
    현재 funSystem에 있는 활동을 가져옴 
"""
def read_data(tree_name="fun_system"):
    dir = db.reference(tree_name)
    return dir.get()

"""
    fun_System DB가 완전히 비어있는 경우 초기화
"""
def insert_funsystem(json_data, root_name="fun_system"):
    try:
        parsed_data = json.loads(json_data)
        print(parsed_data)
        dir = db.reference(root_name)
        dir.set(parsed_data)
    except Exception as e:
        print(traceback.format_exc())


"""
    알림 설정한 부서의 현재 펀시스템 신청 가능한 내역을 반환함
"""
def read_specific_department(departments):
    fun_data = read_data()
    filtered_data = []

    for data in fun_data:
        for department in departments:
            if department in data.get('department'):
                filtered_data.append(data)
                break

    #print(filtered_data)
    return filtered_data

#추후 구현
def update_activity(json_data, root_name='fun_system', ):
    print("추후 구현")


def remove_activity():
    ref = db.reference('fun_system')
    delete_data = ref.order_by_child('remain_date').equal_to("D-day")
    data = delete_data.get()

    for D_day in data:
        ref.child(D_day).delete()

#DB 초기화
def init_db():
    db.reference('fun_system').delete()


#예제 코드
def example():
    return read_specific_department(['IT대학'])


