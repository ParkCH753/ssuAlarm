import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import os
import json
import traceback
from dateutil import relativedelta
from datetime import datetime
from firebase_admin import firestore

load_dotenv()

#firebase db 인증 및 앱 초기화
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred,
                              {'databaseURL' : os.environ.get('DATABASE_URL')}
)

root_name='fun_system'
global_ref = db.reference(root_name)

"""
    현재 funSystem에 있는 활동을 가져옴 
"""
def read_data(tree_name="fun_system"):
    dir = db.reference(tree_name)
    exisitingData = dir.get()
    filteringNone = [data for data in exisitingData if data is not None]
    return filteringNone

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


def read_new_post():
    fun_data = read_data()
    # 'start_date'를 기준으로 최근 10개 프로그램 저장
    recent_programs = sorted(fun_data, key=lambda x: datetime.strptime(x['start_date'],
                                 '%Y-%m-%d'), reverse=True)[:20]
    return recent_programs


# 'remain_date'를 기준으로 가장 적은 날 수로 정렬하고 10개 프로그램 저장
def get_remaining_days(remain_date):
    if remain_date.startswith('D-'):
        if(remain_date=='D-day') :
            return 0
        return int(remain_date[2:])
    return 9999


def read_closest_deadline():
    fun_data=read_data()
    closest_deadline_post = sorted(fun_data,
                 key=lambda x: get_remaining_days(x['remain_date']))[:20]

    return closest_deadline_post


'''
    남은 날짜를 하루씩 땡긴다. D-day인 활동은 제거한다. 
'''
def update_activity(root_name='fun_system'):
    keys = global_ref.get(False, True)
    xx = [*keys]
    delete_count = 0;
    for x in xx:
        update = global_ref.child(x).get()
        remain_date = update['remain_date']
        if remain_date == 'D-1':
            remain_date = 'D-day'
        elif remain_date == 'D-day':
            global_ref.child(x).delete()
            continue
        elif remain_date != 'D-day':
            integer = int(remain_date[2:]) - 1
            remain_date = remain_date[:2] + str(integer)
        update['remain_date'] = remain_date
        global_ref.child(x).update(update)


    print("업데이트 완료.")
    print("제거한 데이터 : ", delete_count)

'''
    기존에 존재하는 데이터에서 데이터 추가 
'''
def add_new_activity(json_data, root_name='fun_system'):
    parsed_data = json.loads(json_data)
    exisitingData = read_data()
    filteringNone = [data for data in exisitingData if data is not None]
    add_list = []
    for new_data in parsed_data:
        flag = True
        for ed in filteringNone:
            if new_data['title'] in ed['title'] :
                flag = False
                break
        if flag is True :
            add_list.append(new_data)
    if add_list : #추가할 데이터가 있으면
        print(add_list)
        last_key_num = get_last_key()
        increment = 1
        for add in add_list:
            db.reference(root_name).child(str(last_key_num + increment)).set(add)
            increment += 1
        print("추가한 데이터 : ", (increment-1))
    else :
        print("추가할 액티비티가 없습니다!")

'''
    기한 지난 데이터 삭제 --> 사용 X 
'''
# def remove_activity():
#     ref = db.reference('fun_system')
#     delete_data = ref.order_by_child('remain_date').equal_to("D-Day")
#     data = delete_data.get()
#     print(data)
#     count = 0
#     for d_day in data:
#         count += 1
#          #ref.child(D_day).delete()
#     print(count)

#DB 초기화
def init_db():
    db.reference('fun_system').delete()

#예제 코드
def example():
    return read_specific_department(['IT대학'])

def get_last_key():
    return int(list(db.reference('fun_system').order_by_key().limit_to_last(1).get().keys())[0])

