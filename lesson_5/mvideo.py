from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

xpath = "//div[contains(text(), 'Хиты продаж')]/../../.."
btn_xpath = "//a[contains(@class, 'next-btn')]"
item_xpath = "//li[contains(@class, 'gallery-list-item')]//h4"

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)

driver.get('https://www.mvideo.ru/')

button = WebDriverWait(driver, 5).until(
    ec.presence_of_element_located((By.XPATH, xpath + btn_xpath))
)

action = ActionChains(driver).move_to_element(button)
action.perform()

while True:

    if button.is_displayed():
        button.click()
    else:
        break

items = driver.find_elements_by_xpath(xpath + item_xpath)
names = []

for item in items:
    names.append(item.text)

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
goods = db.goods

for name in names:

    item = {'name': name}

    goods.insert_one(item)

driver.close()
