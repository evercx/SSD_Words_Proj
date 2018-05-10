from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


browser = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")

# try:
#     browser.get("https://www.taobao.com")
#     input = browser.find_element_by_id('q')
#     input.send_keys('iPhone')
#     time.sleep(2)
#     input.clear()
#     input.send_keys('iPad')
#     input.send_keys(Keys.ENTER)
#     # button = browser.find_element_by_class_name('btn-search')
#     button = browser.find_element(By.CLASS_NAME,'btn-search')
#     button.click()
#     # print(browser.page_source)
# finally:
#     browser.close()


def demo2():
    url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
    browser.get(url)
    browser.switch_to.frame('iframeResult')
    source = browser.find_element_by_css_selector('#draggable')
    target = browser.find_element_by_css_selector('#droppable')
    actions = ActionChains(browser)
    actions.drag_and_drop(source,target)
    actions.perform()

# demo2()





