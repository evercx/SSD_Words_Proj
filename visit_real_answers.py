
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import requests
from pymongo import MongoClient
import csv


# 初始化一个浏览器模拟人操作网页
def init_browser():

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    browser = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")

    return browser

# 从首页获取各个主题下的各个板块下的各个话题的url
def get_topics_urls(browser):

    themes_url = "https://www.thebump.com/real-answers/themes"

    result = []

    browser.get(themes_url)
    print("get success")

    # 绿色导航条的三个主题 依次遍历取下面的元素
    themes_navs = browser.find_elements(By.CLASS_NAME, "ra-green-btn")
    themes_list = ["pregnancy-themes", "parenting-themes", "getting-pregnant-themes"]

    for i in range(3):
        current_element_dict = {}

        current_element_dict["theme_name"] = themes_list[i]
        print(themes_list[i])

        themes_navs[i].click()
        themes_element = browser.find_element(By.CLASS_NAME, themes_list[i])

        # 获取单个主题下的所有boards
        boards = themes_element.find_elements(By.CLASS_NAME, "theme")

        for j in range(len(boards)):

            board_name  =  boards[j].get_attribute("data-name")
            boards[j].click()
            print(board_name)


            cards = browser.find_elements(By.CLASS_NAME, "topic-card")

            for k in range(len(cards)):
                # cards[k].click()
                topic_name = cards[k].find_element(By.TAG_NAME, 'a').find_element(By.CLASS_NAME, 'card-name').text
                href = cards[k].find_element(By.TAG_NAME, 'a').get_attribute('href')

                result.append({
                    "theme_name":themes_list[i],
                    "board_name":board_name,
                    "topic_name":topic_name,
                    "topic_url":href
                })

    print(result)
    return result


# 从HTML代码中找到话题id 为后续请求问题API 拼接请求地址字符串
def get_topicid_from_html(html):

    id_index = html.find("gon.topic_id")
    id_html = html[id_index:]
    start_index = id_html.find("=")
    end_index = id_html.find(";")

    return id_html[start_index+1:end_index]


# 根据给定的话题列表  根据每个话题的网址，爬取它包含的所有问题相关信息
def from_url_get_questions_data(topic_list):

    rs = requests.Session()

    question_url = "https://www.thebump.com/real-answers/v1/topics/{topic_id}/questions"

    # r = question_url.format(topic_id="123")
    # print(r)

    questions_data_list = []
    print("开始爬取")
    for i in range(len(topic_list)):
        topic_url = topic_list[i]["topic_url"]
        html_from_topic = rs.get(topic_url).text
        topic_id = get_topicid_from_html(html_from_topic)


        request_params = {
            "include_user": "true",
            "page_num": 1,
            "page_size": 18
        }

        res = rs.get(question_url.format(topic_id=topic_id), params=request_params).json()
        # print(res)

        request_params["page_size"] = res["total"]

        result_json = rs.get(question_url.format(topic_id=topic_id), params=request_params).json()

        result_json_questions = result_json["questions"]

        for j in range(len(result_json_questions)):

            questions_data_list.append({
                "topic_url":topic_url,
                "id":result_json_questions[j]["id"],
                "title":result_json_questions[j]["title"],
                "created_at":result_json_questions[j]["created_at"],
                "theme_name":topic_list[i]["theme_name"],
                "board_name":topic_list[i]["board_name"],
                "topic_name":topic_list[i]["topic_name"],
                "user_id":result_json_questions[j]["user"]["id"]
            })


    return questions_data_list

#
# def associate_collections():
#
#     conn = MongoClient("121.42.236.250",27034)
#     url_cur = conn.RealAnswers["ElementsURL"].find()
#
#     questions_collection = conn.RealAnswers["Questions"]
#
#     url_list = [ item for item in url_cur]
#
#     for url_item in url_list:
#         condition = {"topic_url":url_item["topic_url"]}
#         set_option = {'$set': {
#             "theme_name":url_item["theme_name"],
#             "board_name": url_item["board_name"],
#             "topic_name": url_item["topic_name"]
#         }}
#
#         result = questions_collection.update_many(condition,set_option)
#         print(result.matched_count, result.modified_count)
#
#     print("关联完毕")


def write_data_to_csv_file():
    conn = MongoClient("121.42.236.250",27034)
    q_cur = conn.RealAnswers["Questions"].find()
    # question_list = [item for item in q_cur]

    row_name = ["topic_name","id","title","user_id","created_at","board_name","theme_name","topic_url"]

    topic_url = []
    id = []
    title = []
    created_at =[]
    theme_name = []
    board_name = []
    topic_name = []

    i = 0
    rows = []
    for item in q_cur:
        i +=1
        current_row = []
        current_row.append(item["topic_name"])
        current_row.append(item["id"])
        current_row.append(item["title"])
        current_row.append(item["user_id"])
        current_row.append(item["created_at"])
        current_row.append(item["board_name"])
        current_row.append(item["theme_name"])
        current_row.append(item["topic_url"])

        rows.append(current_row)

        if i % 500 == 0:
            print("已遍历了",i,"次")

    with open("questions.csv","w",encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(row_name)
        writer.writerows(rows)

        print("写入完毕")




if __name__ == '__main__':

    # browser = init_browser()
    #
    # result_list = get_topics_urls(browser)
    #
    # conn = MongoClient("121.42.236.250",27034)
    # conn.RealAnswers["ElementsURL"].insert(result_list)
    # print("保存成功")

    try:

        conn = MongoClient("121.42.236.250",27034)
        topic_list_cur = conn.RealAnswers["ElementsURL"].find()
        topic_list = [ i for i in topic_list_cur]

        print(topic_list)

        questions_data_list = from_url_get_questions_data(topic_list)

        conn.RealAnswers["Questions"].insert(questions_data_list)
        print("保存成功")

    except Exception as e:
        print(e)

    # associate_collections()
    # write_data_to_csv_file()


