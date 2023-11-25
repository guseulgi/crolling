from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import json
import src

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/nametoproj', methods=['GET', 'POST'])
def nametoproj():
    if request.method == 'GET':
        return render_template('nametoproj.html')

    if request.method == 'POST':
        # 사용자 입력 받기
        name = str(request.form.get('name', ''))

        # 셀레니움 실행 함수
        src.functions.nametoproj(name)
        return render_template('nametoproj.html', name=name)


@app.route('/retrieveadm')
def retrieveadm():
    return render_template('retrieveadm.html')


if __name__ == '__main__':
    app.run(debug=True)
