from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from dotenv import load_dotenv
import os
import re


tmpdic = {}


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
    time.sleep(.1)

    idInput = driver.find_element(By.CSS_SELECTOR, "#username")
    pwInput = driver.find_element(By.CSS_SELECTOR, "#password")

    idInput.send_keys(os.environ.get('REDMINE_ID'))
    pwInput.send_keys(os.environ.get('REDMINE_PW'))
    submitBtn = driver.find_element(By.CSS_SELECTOR, "#login-submit")
    submitBtn.click()
    time.sleep(.1)

    # 로그인 후 초기화면 > 관리 > 그룹
    magBtn = driver.find_element(
        By.CSS_SELECTOR, "#top-menu > ul > li:nth-child(4) > a")
    magBtn.click()
    time.sleep(.1)

    groupBtn = driver.find_element(
        By.CSS_SELECTOR, "#admin-menu > ul > li:nth-child(3) > a")
    groupBtn.click()
    time.sleep(.1)

    # 각 그룹의 프로젝트 페이지 > 프로젝트 안 구성원을 받아온 이름과 매칭
    groups = driver.find_elements(
        By.CSS_SELECTOR, "#content > div.autoscroll > table > tbody > tr > td.name > a")

    for group in groups:
        print('그룹: ', group.text)
        group.click()
        time.sleep(.1)

        userBtn = driver.find_element(By.CSS_SELECTOR, "#tab-users")
        userBtn.click()
        time.sleep(.1)

        users = driver.find_elements(
            By.CSS_SELECTOR, "#tab-content-users > table > tbody > tr > td.name > a.user")

        for user in users:
            usr = re.sub(r"[^가-힣]", '', user.text)
            # print(searchInput, usr)
            if searchInput == usr:
                projBtn = driver.find_element(
                    By.CSS_SELECTOR, "#tab-memberships")
                projBtn.click()
                time.sleep(.1)

                projs = driver.find_elements(
                    By.CSS_SELECTOR, "#tab-content-memberships > table > tbody > tr > td.project > a")
                for proj in projs:
                    projname = proj.text
                    proj.click()
                    time.sleep(.1)

                    members = driver.find_elements(
                        By.CSS_SELECTOR, "#content > div.splitcontent > div.splitcontentright > div > p > a")
                    for member in members:
                        memname = re.sub(r"[^가-힣]", '', member.text)
                        if searchInput == memname:
                            time.sleep(.1)
                            if tmpdic.get(searchInput) == None:
                                tmpdic[searchInput] = [projname]
                            else:
                                tmpdic[searchInput].append(projname)
                            # print(tmpdic, '!!!!')

                        if members[-1] == member:
                            driver.back()
                            time.sleep(0.1)
                            break
                        else:
                            continue

            if users[-1] == user:
                driver.back()
                time.sleep(0.1)
                break
            else:
                continue

        if searchInput in tmpdic:
            # 필터링이 끝나면 드라이버 종료
            driver.quit()
            return tmpdic
        else:
            continue
