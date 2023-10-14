from flask import Flask, jsonify, request
import sys, random, json, datetime
application = Flask(__name__)


@application.route("/hello",methods=['GET'])
def hello():
	return "Hello!"


@application.route("/animal", methods=['POST'])
def animal():
    req = request.get_json()
    print(req)
    animal_type = req["action"]["detailParams"]["Animal_type"]["value"]	# json파일 읽기
    print(animal_type)
    answer = animal_type
    # 답변 텍스트 설정
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    # 답변 전송
    return jsonify(res)


@application.route("/random", methods=["POST"])
def random_function():
    answer = random.randrange(1, 10)
    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(answer) 
                    }
                }
            ]
        }
    }
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
    response = {
        "version": "2.0",
        "templete": {
            "outputs": [
                {
                    "simpleText": {
                        # 요일정보를 받아와 글자로 치환하여 출력
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(response)


@application.route("/category",methods=["POST"])
def category_list():
	response = {
		"version": "2.0",
		"template": {
			"outputs": [
			{
				"carousel": {
					"type": "basicCard",
					"items": [
					{
						"title": "보물상자",
						"description": "보물상자 안에는 뭐가 있을까",
						"thumbnail": {
							"imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/lj3JUcmrzC53YIjNDkqbWK.jpg"
						},
						"buttons": [
						{
							"action": "message",
							"label": "열어보기",
							"messageText": "짜잔! 우리가 찾던 보물입니다"
						},
						{
							"action":  "webLink",
							"label": "구경하기",
							"webLinkUrl": "https://e.kakao.com/t/hello-ryan"
						}
						]
					},
					{
						"title": "보물상자2",
						"description": "보물상자2 안에는 뭐가 있을까",
						"thumbnail": {
							"imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/lj3JUcmrzC53YIjNDkqbWK.jpg"
						},
						"buttons": [
						{
							"action": "message",
							"label": "열어보기",
							"messageText": "짜잔! 우리가 찾던 보물입니다"
						},
						{
							"action":  "webLink",
							"label": "구경하기",
							"webLinkUrl": "https://e.kakao.com/t/hello-ryan"
						}
						]
					},
					{
						"title": "보물상자3",
						"description": "보물상자3 안에는 뭐가 있을까",
						"thumbnail": {
							"imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/lj3JUcmrzC53YIjNDkqbWK.jpg"
						},
						"buttons": [
						{
							"action": "message",
							"label": "열어보기",
							"messageText": "짜잔! 우리가 찾던 보물입니다"
						},
						{
							"action":  "webLink",
							"label": "구경하기",
							"webLinkUrl": "https://e.kakao.com/t/hello-ryan"
						}
						]
					}
					]
				}
			}
			]
		}
	}
	return jsonify(response)



if __name__ == "__main__":
	application.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)

