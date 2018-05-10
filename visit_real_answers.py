
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import requests
from pymongo import MongoClient


# 初始化一个浏览器模拟人操作网页
def init_browser():

    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    browser = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")

    return browser


def demo(browser):

    themes_url = "https://www.thebump.com/real-answers/themes"

    # themes_url = "file:///Users/evercx/Desktop/themes/Pregnancy%20and%20Parenting%20Message%20Boards.htm"

    browser.get(themes_url)
    print("get success")

    # theme_li = browser.find_element(By.CLASS_NAME,"ra-green-btn")


    themes_navs = browser.find_elements(By.CLASS_NAME,"ra-green-btn")
    current_themes_index = 1
    themes_navs[current_themes_index].click()
    themes_list = ["pregnancy-themes", "parenting-themes", "getting-pregnant-themes"]
    themes_element = browser.find_element(By.CLASS_NAME,themes_list[current_themes_index])

    boards = themes_element.find_elements(By.CLASS_NAME,"theme")
    print(boards)
    boards[0].click()
    print(boards[0].get_attribute("data-name"))

    cards = browser.find_elements(By.CLASS_NAME,"topic-card")
    href = cards[0].find_element(By.TAG_NAME,'a').get_attribute('href')
    print(href)
    topic_name = cards[0].find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'card-name').text;
    print(topic_name)


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


def get_topicid_from_html(html):

    id_index = html.find("gon.topic_id")
    id_html = html[id_index:]
    start_index = id_html.find("=")
    end_index = id_html.find(";")

    return id_html[start_index+1:end_index]


def from_url_get_questions_data(topic_list):

    rs = requests.Session()

    question_url = "https://www.thebump.com/real-answers/v1/topics/{topic_id}/questions"

    # r = question_url.format(topic_id="123")
    # print(r)

    questions_data_list = []
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
        print(res)

        request_params["page_size"] = res["total"]

        result_json = rs.get(question_url.format(topic_id=topic_id), params=request_params).json()

        result_json_questions = result_json["questions"]

        for j in range(len(result_json_questions)):

            questions_data_list.append({
                "topic_url":topic_url,
                "id":result_json_questions[j]["id"],
                "title":result_json_questions[j]["title"],
                "created_at":result_json_questions[j]["created_at"]
            })

    return questions_data_list

















if __name__ == '__main__':

    # browser = init_browser()
    #
    # result_list = get_topics_urls(browser)
    #
    # conn = MongoClient("121.42.236.250",27034)
    # conn.RealAnswers["ElementsURL"].insert(result_list)
    # print("保存成功")

    conn = MongoClient("121.42.236.250",27034)
    topic_list_cur = conn.RealAnswers["ElementsURL"].find()

    topic_list = [ i for i in topic_list_cur]

    print(topic_list)

    questions_data_list = from_url_get_questions_data(topic_list)

    print(questions_data_list)

    print("爬取成功")
