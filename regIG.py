from codecs import unicode_escape_decode
from datetime import datetime
import threading, time, requests, random, re,string,pyautogui,json,os,pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
#import subprocess
#module_names = ["selenium", "fake_useragent", "unidecode","pyautogui","requests"]
#for module_name in module_names:
    #try:
        #subprocess.check_call(["pip", "install", module_name])
    #except:
        #pass
class Instagram(object):
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie
        self.xcsrftoken = cookie.split("csrftoken=")[1].split(';')[0]
        try:
            headers = {
                'accept': "*/*",
                'authority': "www.instagram.com",
                'content-type': "application/x-www-form-urlencoded",
                'cookie': self.cookie,
                'user-agent': f"Mozilla/5.0 (Windows NT {random.choice(['7', '8', '10', '11'])}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 104)}.0.0.0 Safari/537.36",
                'x-csrftoken': self.xcsrftoken,
            }
            post = requests.get("https://www.instagram.com/", headers=headers).text
            self.idProfile = post.split('''"viewerId":"''')[1].split('"}')[0]
            self.x_instagram_ajax = post.split('''rollout_hash":''')[1].split('",')[0]
            self.appId = post.split('''"appId":"''')[1].split('","')[0]
            self.name = json.loads(unicode_escape_decode(post.split('full_name\\":')[1].split(',\\"')[0])[0])
            self.headersApi = {
                'accept': "*/*",
                'authority': "www.instagram.com",
                'content-type': "application/x-www-form-urlencoded",
                'cookie': self.cookie,
                'user-agent': f"Mozilla/5.0 (Windows NT {random.choice(['7', '8', '10', '11'])}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 104)}.0.0.0 Safari/537.36",
                'x-csrftoken': self.xcsrftoken,
                'x-requested-with': "XMLHttpRequest",
                'x-ig-app-id': self.appId,
                'x-instagram-ajax': self.x_instagram_ajax,
            }
        except:
            pass
    
    # def getInfoCookie(self) -> string:
    #     try:
    #         try:
    #             id = self.idProfile
    #             name = self.name
    #         except:
    #             self.setValues()
    #             id = self.idProfile
    #             name = self.name
    #         return id, name
    #     except:
    #         pass
    def followUser(self, id: int, proxy = None) -> bool:
        try:
            if proxy != None:
                postFollow = requests.post(f"https://i.instagram.com/api/v1/web/friendships/{id}/follow/", headers=self.headersApi, proxies=self.proxyDict).json()
            else:
                postFollow = requests.post(f"https://i.instagram.com/api/v1/web/friendships/{id}/follow/", headers=self.headersApi).json()
            if postFollow['result'] == "following" and postFollow['status'] == "ok":
                return True
            else:
                return False
        except:
            return False 
    def up_avt(self, img_path: str, proxy = None):
        try:
            headers = {
                'user-agent': f"Mozilla/5.0 (Windows NT {random.choice(['7', '8', '10', '11'])}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 104)}.0.0.0 Safari/537.36",
                "accept": "*/*",
                "accept-Language": "en-US,en;q=0.5",
                "accept-Encoding": "gzip, deflate, br",
                "referer": "https://www.instagram.com/",
                'x-csrftoken': self.xcsrftoken,
                'x-requested-with': "XMLHttpRequest",
                'x-ig-app-id': self.appId,
                'x-instagram-ajax': self.x_instagram_ajax,
                "content-length": str(os.path.getsize(img_path)),
                "DNT": "1",
                "x-asbd-id": "198387",
                "connection": "keep-alive",
                "cookie": self.cookie
            }
            if proxy != None:
                upAvt = requests.post("https://i.instagram.com/api/v1/web/accounts/web_change_profile_picture/", files = {'profile_pic': open(img_path,'rb')}, data={"Content-Disposition": "form-data", "name": "profile_pic", "filename":"profilepic.jpg","Content-Type": "image/jpeg"}, headers=headers, proxies=self.proxyDict).json()
            else:
                upAvt = requests.post("https://i.instagram.com/api/v1/web/accounts/web_change_profile_picture/", files = {'profile_pic': open(img_path,'rb')}, data={"Content-Disposition": "form-data", "name": "profile_pic", "filename":"profilepic.jpg","Content-Type": "image/jpeg"}, headers=headers).json()
            if upAvt['changed_profile'] == True:
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def up_load_post(self, img_path: str, *caption, proxy = None) -> bool:
        if caption:
            caption = caption[0]
        #print(img_path, caption, proxy)
        try:
            upload_id = int(datetime.now().timestamp())
            url_load_img = "https://i.instagram.com/rupload_igphoto/fb_uploader_{}".format(upload_id)
            headers = {
                'content-type': "image/jpeg",
                'cookie': self.cookie,
                'offset': "0",
                'user-agent': f"Mozilla/5.0 (Windows NT {random.choice(['7', '8', '10', '11'])}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 104)}.0.0.0 Safari/537.36",
                'x-csrftoken': self.xcsrftoken,
                'x-requested-with': "XMLHttpRequest",
                'x-entity-length': str(os.path.getsize(img_path)),
                'x-entity-name': "fb_uploader_{}".format(upload_id),
                'x-ig-app-id': self.appId,
                'x-instagram-ajax': self.x_instagram_ajax,
                'x-instagram-rupload-params': f'{{"media_type":1,"upload_id":"{upload_id}","upload_media_height":780,"upload_media_width":780}}',
            }
            dataPost = open(img_path, "rb")
            url_up_post = "https://i.instagram.com/api/v1/media/configure/"
            data = {
                'source_type': "library",
                'caption': str(caption) if caption else "",
                'upload_id': upload_id,
                'disable_comments': "0",
                'like_and_view_counts_disabled': "0",
                'igtv_share_preview_to_feed': "1",
                'is_unified_video': "1",
                'video_subtitles_enabled': "0"
            }
            if proxy != None:
                print(self.proxyDict)
                requests.post(url=url_load_img,data=dataPost, headers=headers, proxies=self.proxyDict).json()
                up_post = requests.post(url = url_up_post, headers = self.headersApi, data = data, proxies=self.proxyDict).json()
            else:
                requests.post(url=url_load_img,data=dataPost, headers=headers).json()
                up_post = requests.post(url = url_up_post, headers = self.headersApi, data = data).json()
            
            if up_post['status'] == "ok":
                return True
            else:
                return False
        except Exception as e:
            return False



class RegAcc(threading.Thread):
    def __init__(self):
        super().__init__()
        self.password = ''
        pass
    def getDriver(self):
        global pos_x,pos_y
        # s = '/path/to/chromedriver'
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--silent')
        # service = Service(executable_path=s)
        driver = webdriver.Chrome(options=options)
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
        driver.set_window_size(500,600)
        driver.set_window_position(pos_x,pos_y)
        pos_x +=400
        if pos_x + 400 > driver.execute_script('return window.screen.width'):
            pos_x = 0
            pos_y += 300
        if pos_y + 500 > driver.execute_script('return window.screen.height'):
            pos_y = 0
        return driver
    def getName(self):
        gender = random.choice(["male", "female"])
        self.nameig = requests.get("https://story-shack-cdn-v2.glitch.me/generators/vietnamese-name-generator/").json()["data"][gender]   
    def randomName(self):
        VIETNAMESE_CHARS = "aAeEoOuUiIdDyY"
        first_names = ['Trần', 'Lê', 'Nguyễn', 'Phạm', 'Huỳnh', 'Đặng', 'Võ', 'Bùi', 'Đỗ', 'Hồ','Văn', 'Thị', 'Duy', 'Thu', 'Tiến', 'Đức', 'Đình', 'Hữu', 'Ngọc', 'Mỹ','An', 'Bình', 'Cường', 'Dũng', 'Hiền', 'Khoa', 'Linh', 'Mạnh', 'Nga', 'Phúc','Tao','Yen','Phụng','Kê','Nam']
        middle_names = ['Trần', 'Lê', 'Nguyễn', 'Phạm', 'Huỳnh', 'Đặng', 'Võ', 'Bùi', 'Đỗ', 'Hồ','Văn', 'Thị', 'Duy', 'Thu', 'Tiến', 'Đức', 'Đình', 'Hữu', 'Ngọc', 'Mỹ','An', 'Bình', 'Cường', 'Dũng', 'Hiền', 'Khoa', 'Linh', 'Mạnh', 'Nga', 'Phúc','Tao','Yen','Phụng','Kê','Nam']
        last_names = ['Trần', 'Lê', 'Nguyễn', 'Phạm', 'Huỳnh', 'Đặng', 'Võ', 'Bùi', 'Đỗ', 'Hồ','Văn', 'Thị', 'Duy', 'Thu', 'Tiến', 'Đức', 'Đình', 'Hữu', 'Ngọc', 'Mỹ','An', 'Bình', 'Cường', 'Dũng', 'Hiền', 'Khoa', 'Linh', 'Mạnh', 'Nga', 'Phúc','Tao','Yen','Phụng','Kê','Nam']
        first_name = random.choice(first_names)
        middle_name = random.choice(middle_names)
        last_name = random.choice(last_names)
        name = f"{first_name}_{middle_name}_{last_name}"
        name = unidecode(name)
        number = random.randint(1000,9999999)
        self.username = f"{name.lower().replace(' ', '_')}{number}"
        return self.username
    
    def randomPassword(self):
        letters = string.ascii_lowercase
        digits = string.digits
        random_letters = ''.join(random.choice(letters) for i in range(5))
        random_digits = ''.join(random.choice(digits) for i in range(4))
        self.password = random_letters + random_digits
        return self.password    

    def randomBirthday(self):
        self.d = str(random.randint(1,30)) 
        self.m = str(random.randint(1,12)) 
        self.y = str(random.randint(1995,2003))

    def GetTMmail(self):
        user = ["a","b","c","d","e","f","g","h","u","i","o","y","m","n","l","h","q","x","s","k","p","t","w","v","j","z"]
        self.mail = ""
        for i in range(4):
            num = str(random.randint(1,100))
            self.mail += random.choice(user)
            self.mail += num
        domain = requests.get("https://api.mail.tm/domains?page=1", headers={"content-type":"application/json"}).json()["hydra:member"][0]["domain"]
        self.mail += "@"+domain
        data = '{"address":"'+self.mail+'","password":"11062003"}'
        acc = requests.post("https://api.mail.tm/accounts", data, headers={"content-type":"application/json"}).json()
        self.token = requests.post("https://api.mail.tm/token", data, headers={"content-type":"application/json"}).json()["token"]
    
    def GetCodeTMmail(self):
        messages = requests.get("https://api.mail.tm/messages",headers={"authorization":"Bearer "+self.token}).text
        c = re.findall(r'subject":".*?code',messages)
        if c == []:
            return ""
        return re.findall(r"\d{6}",c[0])[0]
    
    def run(self):
        while True:
            try:  
                self.randomPassword()
                self.randomName()
                self.GetTMmail()
                self.getName()
                driver = self.getDriver()
                driver.implicitly_wait(20)
                #driver.get("https://www.instagram.com/")
                driver.get("https://www.instagram.com/accounts/emailsignup/")
                driver.implicitly_wait(30)
                driver.find_element(By.NAME, "emailOrPhone").send_keys(self.mail)
                driver.find_element(By.NAME, "fullName").send_keys(self.nameig)
                driver.find_element(By.NAME, "username").send_keys(self.username)
                driver.find_element(By.NAME, "password").send_keys(self.password)
                driver.find_element(By.XPATH, '//button[text()="Sign up"]').click()
                driver.implicitly_wait(30)
                self.randomBirthday()
                birthday = driver.find_elements(By.CLASS_NAME, "_aau-")
                Select(birthday[0]).select_by_value(self.m)
                Select(birthday[1]).select_by_value(self.d)
                Select(birthday[2]).select_by_value(self.y)
                driver.find_element(By.XPATH, '//button[text()="Next"]').click() 
                sleep(15)
                code = self.GetCodeTMmail()
                driver.find_element(By.NAME,"email_confirmation_code").send_keys(code)
                driver.find_element(By.XPATH,"//div[contains(text(),'Next')]").click()
                driver.implicitly_wait(30) 
                notnow = driver.find_element(By.CSS_SELECTOR,'button[class="_a9-- _a9_1"]').click()
                sleep(15)
                follows = driver.find_elements(By.CLASS_NAME,"_aacl")
                count = 0
                for fl in follows:
                    if fl.text == "Follow":
                        actions = ActionChains(driver)
                        actions.move_to_element(fl).click().perform()
                        time.sleep(1)
                        driver.execute_script("window.scrollBy(0, 55);")
                        count += 1 
                    if count == 10:
                        break
                sleep(5)
                #demo follow
                cookies = driver.get_cookies()
                ck = ''
                for cookie in cookies:
                    ck += f"{cookie['name']}={cookie['value']};" 
                ig = Instagram(ck)
                dg = os.getcwd()
                # id_igs = ['57336515500','48262838036','60041053727','5718213645','50797751957','7479061362','56809338299','21687588964','61216590537','892832118']
                # for id_ig in id_igs:
                #     ig.followUser(id_ig,proxy=None)
                # driver.refresh()
                with open('link.txt', 'r') as f:
                    lines = f.readlines()
                random_line = random.choice(lines).strip()
                avtt = os.path.join(dg,random_line)
                ig.up_avt(avtt,  proxy = None)
                for i in range(3):
                    random_line = random.choice(lines).strip()
                    avtt = os.path.join(dg,random_line)        
                    ig.up_load_post(avtt, "dzu", proxy = None)
                with open("accounts.txt", "a") as f:
                    f.write(f"{self.mail}|{self.username}|{self.password}|{ck}\n")
                    print('Reg thành công acount INSTAGRAM !!')
                # with open("cookie.txt", "a") as f:
                #     f.write(f"{ck}\n")
                sleep(2)
                driver.quit()
            except:
                driver.quit()
pos_x = 0
pos_y = 0
modules = int(input('Nhập số luồng : '))
for i in range(modules):
    f = RegAcc()
    f.start()
    sleep(1)

