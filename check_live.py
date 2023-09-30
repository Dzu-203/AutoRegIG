from selenium.webdriver.common.action_chains import ActionChains
import threading,requests, random, re,string,os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

class Check(threading.Thread):
    def __init__(self):
        super().__init__()
        pass
    def getDriver(self):
        s = '/path/to/chromedriver'
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--silent')
        options.add_argument('--headless')
        service = Service(executable_path=s)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    def run(self):
            driver = self.getDriver()
            driver.implicitly_wait(2)
            driver.get("https://www.instagram.com/")
            acc_live = open('live.txt','w')
            acc_die = open('die.txt','w')
            with open('accounts.txt','r') as file:
                for user in file:
                    user = user.split("\n")[0]
                    users = user.split("|")[1].split("|")[0]
                    driver.get(f"https://www.instagram.com/{users}/")
                    driver.implicitly_wait(2)
                    result = driver.find_elements(By.XPATH,'//span[contains(text(),"Sorry, this page isn\'t available.")]')
                    if result:
                        print(f"{users} : DIE")
                        acc_die.write(user + "\n")                        
                    else:
                        print(f"{users} : LIVE")
                        acc_live.write(user + "\n")
f = Check()
f.start()


