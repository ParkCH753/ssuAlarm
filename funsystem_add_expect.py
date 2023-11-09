# Selenium
import json

import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 설치 및 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#예외 출력
import traceback
import database

import re

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("headless")  # 백그라운드에서 작업

# 드라이버 생성 및 열기
service = Service(executable_path=ChromeDriverManager().install())

funSystemURL =  "https://fun.ssu.ac.kr"
path = "/ko/program/all/list/all"
imgUriPattern = r'/attachment/view/\d+/cover\.jpg\?ts=\d+'

def parsing(page, keyword, department):
    # 드라이버 생성 및 열기
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(10)  # 페이지 로딩 시간 대기
    fun_list = []
    fun_list_expected = []
    flag = True
    while flag:
        try:
            browser.get(funSystemURL + path + "/" + str(page)) #해당 페이지 브라우저 열기
            page += 1
            fun_html_body =  browser.find_element(By.CLASS_NAME, "columns-4") #메인 바디 html 얻기
            fun_html_list = fun_html_body.find_elements(By.TAG_NAME, "a") # <a> 태그 값 얻기
            for fun_html in fun_html_list :
                #크롤링하는 날짜 오늘 기준 남은 날짜
                day = fun_html.find_element(By.CSS_SELECTOR, "label > b").text
                if ("종료" in day) or ("마감" in day):
                    flag = False
                    break #종료된 것 or 예정인 것이 나오면 break.

                #상세 경로 추출
                url = fun_html.get_attribute("href")  # 링크 얻기

                # 부서 추출
                institution = fun_html\
                    .find_element(By.CLASS_NAME, "content").find_element(By.CLASS_NAME, "department")\
                    .find_element(By.CLASS_NAME, "institution").text

                #서브 부서 타입 (단과대, 개설학과 꼴)
                subDepartment = fun_html\
                    .find_element(By.CLASS_NAME, "content").find_element(By.CLASS_NAME, "department")\
                    .find_element(By.CLASS_NAME, "department").text

                department = institution
                if subDepartment != "" : #서브 부서가 있다면
                    department = department + " " + subDepartment

                # 제목 추출
                title = fun_html.find_element(By.CLASS_NAME, "content").find_element(By.CLASS_NAME, "title_wrap")\
                    .find_element(By.CLASS_NAME, "title").text

                #시작, 마감날짜 추출
                small_tag = fun_html.find_element(By.CLASS_NAME, "content").find_elements(By.TAG_NAME, "small")

                signup = small_tag[2]
                #operation = small_tag[3]

                # 이미지 URI 추출
                img_uri = fun_html.find_element(By.CLASS_NAME, "cover").get_attribute("style")
                parsingImgUri = re.search(imgUriPattern, img_uri)
                fullImgUrl = funSystemURL + parsingImgUri.group()

                #시작 날짜
                time = signup.find_elements(By.TAG_NAME, "time")
                start_date = time[0].get_attribute("datetime").split('T')[0]
                dead_line = time[1].get_attribute("datetime").split('T')[0]

                # #운영 기간
                # time = operation.find_elements(By.TAG_NAME, "time")
                # oper_start_date = time[0].get_attribute("datetime")
                # oper_dead_line = time[1].get_attribute("datetime")
                if "예정" in day:
                    program = Program(title = title, department = department, url = url, start_date=start_date, end_date=dead_line, remain_date=day, img_url=fullImgUrl)
                    fun_list_expected.append(program)
                else:
                    if "임박" in day : day = "D-day" #임박이면 오늘 끝나는 것.
                    program = Program(title = title, department = department, url = url, start_date=start_date, end_date=dead_line, remain_date=day, img_url=fullImgUrl)
                    fun_list.append(program)


                

        #10초 이네에 페이지 로딩이 다 안되는 경우 ---> 펀시스템 에러
        except selenium.common.ElementNotVisibleException :
            return None

        except Exception as ex:
            traceback.print_exception()
            break

    #dto = Dto(fun_list, fun_list_expected)
    return fun_list, fun_list_expected


class Program:
    def __init__(self, title, department, url, start_date, end_date, remain_date, img_url):
        self.title = title #프로그램 이름
        self.department = department #설계 부서
        self.URL = url #해당 펀시스템 url
        self.start_date = start_date
        self.end_date = end_date
        self.remain_date = remain_date
        self.img_uri = img_url

    def __str__(self):
        return 'title : %s, department : %s, start_date = %s, end_date = %s, remain_date = %s, url = %s '%(self.title, self.department, self.start_date, self.end_date, self.remain_date, self.URL)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent = 4, ensure_ascii=False)

def to_json(fun_list):
    return json.dumps(fun_list, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    info_curr, info_expect = parsing(page=1, keyword=None, department=None)
    #database.insert_funsystem(to_json(info_curr))

