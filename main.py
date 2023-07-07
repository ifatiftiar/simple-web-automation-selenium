import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(url):
    # set options to make browsing easier
    options = Options()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option("detach", True)
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    return driver


def clean_text(text):
    """Extract only the temperature from the text"""
    output = float(text.split(": ")[1])
    return output


def read_text():
    driver = get_driver("https://automated.pythonanywhere.com/")
    time.sleep(2)
    # element = driver.find_element('xpath', '/html/body/div[1]/div/h1[1]')
    element = driver.find_element(by='xpath', value='/html/body/div[1]/div/h1[2]')
    return clean_text(element.text)


def login():
    driver = get_driver('https://automated.pythonanywhere.com/login/')
    username = driver.find_element(by='id', value='id_username')
    username.send_keys('automated')

    time.sleep(2)

    password = driver.find_element(by='id', value='id_password')
    password.send_keys('automatedautomated' + Keys.RETURN)

    time.sleep(2)

    home = driver.find_element(by='xpath', value='/html/body/nav/div/a')
    home.click()

    time.sleep(2)

    element = driver.find_element(by='xpath', value='/html/body/div[1]/div/h1[2]')

    return clean_text(element.text)


def read_temperature_and_write_to_file():
    count = 3
    while True:
        time.sleep(2)
        temperature = str(read_text())
        date = datetime.now()
        filename = date.strftime("%Y-%m-%d.%H-%M-%S.txt")

        f = open(filename, 'x')
        f.write(temperature)
        f.close()

        count -= 1

        if count <= 0:
            break


read_temperature_and_write_to_file()

