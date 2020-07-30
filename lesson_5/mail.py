from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


login = 'study.ai_172@mail.ru'
password = 'NextPassword172'

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)

driver.get('https://mail.ru/')
login_field = driver.find_element_by_id('mailbox:login')
login_field.send_keys(login)
pass_btn = driver.find_element_by_xpath("//input[@class='o-control']")
pass_btn.click()
pass_field = driver.find_element_by_id('mailbox:password')
pass_field.send_keys(password)
mem_box = driver.find_element_by_xpath("//label[contains(@class, 'mailbox__control_saveauth')]")
mem_box.click()
pass_btn.click()

links = set()
last_letter = None

while True:

    letters = WebDriverWait(driver, 10).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'js-letter-list-item'))
            )

    if last_letter == letters[-1]:
        break

    last_letter = letters[-1]

    for letter in letters:
        links.add(letter.get_attribute('href'))

    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()

links = list(links)
data = []

for link in links:

    item = {}
    driver.get(link)

    item['theme'] = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))
    ).text

    item['from'] = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//div[@class='letter__author']/span"))
    ).text

    item['date'] = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'letter__date'))
    ).text

    item['body'] = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'letter__body'))
    ).text

    data.append(item)

    driver.back()


client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru']
goods = db.letters

for letter in data:
    goods.insert_one(letter)

driver.close()
