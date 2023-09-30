import threading, time, requests, random, re,string,pyautogui,json,os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import string
import requests, json, random, os
import random

class Get():
    def __init__(self):
        super().__init__()
        pass
    def getDriver(self):
        s = '/path/to/chromedriver'
        options = Options()
        driver = webdriver.Chrome(executable_path=s, options=options)
        return driver
    
    def run(self):
         with open('accounts.txt', 'r') as file:
            for tk in file:
                user = tk.split("|")[1]
                password = tk.split("|")[2]
                driver = self.getDriver()
                Login = driver.get("https://www.instagram.com/")
                driver.implicitly_wait(20)
                users = driver.find_element(By.NAME,'username').send_keys(user)
                passwords = driver.find_element(By.NAME,'password').send_keys(password)
                login = driver.find_element(By.XPATH,'//div[text()="Log in"]').click()
                not_now = driver.find_element(By.XPATH,'//div[text()="Not Now"]').click()
                notnow = driver.find_element(By.CSS_SELECTOR,'button[class="_a9-- _a9_1"]').click()
                time.sleep(5)
                cookies = driver.get_cookies()
                cookie_str = ''
                for cookie in cookies:
                    cookie_str += f"{cookie['name']}={cookie['value']};"
                with open('cookie.txt','a') as f:
                    f.write(f"{cookie_str}\n")
f = Get()
f.run()

