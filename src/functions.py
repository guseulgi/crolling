from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from dotenv import load_dotenv
import os


def nametoproj(searchInput):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    load_dotenv()

    # 페이지 오픈
    url = os.environ.get('REDMINE_MAIN')
    driver.get(url)
    time.sleep(1)

    # 로그인
    loginBtn = driver.find_element(
        By.CSS_SELECTOR, "#account > ul > li:nth-child(1) > a")
    loginBtn.click()

    idInput = driver.find_element(By.CSS_SELECTOR, "#username")
    pwInput = driver.find_element(By.CSS_SELECTOR, "#password")

    idInput.send_keys(os.environ.get('REDMINE_ID'))
    pwInput.send_keys(os.environ.get('REDMINE_PW'))
    submitBtn = driver.find_element(By.CSS_SELECTOR, "#login-submit")
    submitBtn.click()

    # 로그인 후 초기화면 > 관리 > 그룹
    magBtn = driver.find_element(
        By.CSS_SELECTOR, "#top-menu > ul > li:nth-child(4) > a")
    magBtn.click()

    groupBtn = driver.find_element(
        By.CSS_SELECTOR, "#admin-menu > ul > li:nth-child(3) > a")
    groupBtn.click()

    # 각 그룹의 프로젝트 페이지 > 프로젝트 안 구성원을 받아온 이름과 매칭
    groups = driver.find_elements(
        By.CSS_SELECTOR, "#content > div.autoscroll > table > tbody > tr > td.name > a")
    # print(groups)

    for group in groups:
        userBtn = driver.find_element(By.CSS_SELECTOR, "#tab-users")
        userBtn.click()
