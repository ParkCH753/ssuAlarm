from flask import Flask, jsonify, request
import sys, random, json, datetime
import kakao_response as kakao
import database as db
from pprint import pprint
#from apscheduler.schedulers.background import BackgroundScheduler
application = Flask(__name__)

# def printest():
# 	return print_file.printf()
#
# sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
# sched.add_job(printest, 'interval', seconds=2)
# sched.start()

@application.route("/random", methods=["POST"])
def random_function():
	answer = random.randrange(1, 10)
	response = kakao.simple_text(str(answer))

	print(response)
	return response


days_of_the_week_list = ['월', '화', '수', '목', '금', '토', '일']
@application.route("/day", methods=["POST"])
def day_of_the_week():
	# part1 - 카카오톡 서버에서 스킬이 보내는 보내는 요청의 데이터
	request_data = json.loads(request.get_data(), encoding='utf-8')
	print(request_data)
	# part2 - ge date params
	# 파라미터에서 날짜 파라미터의 값 가져오기(문자열로 되어 있으므로 별도로 json으로 변환할 필요가 있음)
	params = request_data['action']['params']  # 파라미터 가져오기
	print(params)
	param_date = json.loads(params['sys_date_params'])  # 파라미터 중 날짜 파라미터 가져오기
	print(param_date)
	# 해당 날짜를 (파이썬의 날짜/시간 저장형식 인) datetime 형식으로 저장하기(년도 정보 없는 경우 현재 년도로)
	date_obj = datetime.datetime(
		int(param_date['year']) if param_date['year'] else datetime.datetime.today().year,
		int(param_date['month']),
		int(param_date['day'])
	)
	answer = days_of_the_week_list[date_obj.weekday()] + "요일"
	response = kakao.simple_text(answer)
	return jsonify(response)


@application.route("/fun_closest",methods=["POST"])
def fun_closest():

	data=db.read_closest_deadline()

	res = basic_card_carousel_fun(data)

	return res


@application.route("/fun_new",methods=["POST"])
def fun_new():

	# db에서 데이터 불러오기
	data = db.read_new_post()
	#pprint(data)

	res = basic_card_carousel_fun(data)

	return res


@application.route("/fun_department",methods=["POST"])
def fun_department():
	# 파라미터에서 부서 불러오기
	request_data = json.loads(request.get_data(as_text=True))
	params = request_data['action']['params']
	#pprint(params)
	param_departments = params['fun_department']
	#pprint(param_departments)

	# department를 list로 만듬
	department_list=[]
	department_list.append(param_departments)

	# db에서 데이터 불러오기
	data = db.read_specific_department(department_list)
	#pprint(data)
	
	res=basic_card_carousel_fun(data)

	return res


def basic_card_carousel_fun(data):

	if(len(data)==0) :
		return kakao.simple_text("해당하는 게시글이 없습니다.")

	# 데이터 블록화 하기
	items=[]
	for post in data :
		button = kakao.to_button("webLink","web으로 보기",
								webLinkUrl=post['URL'])
		pprint(button)
		description=f"{post['end_date']} 마감. / {post['remain_date']}"
		item=kakao.to_item(post['title'],description, post['img_uri'] ,[button])

		pprint(item)
		items.append(item)
	
	res = kakao.basic_card_carousel(items)

	return res
	



if __name__ == "__main__":
	application.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)



