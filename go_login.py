import psutil
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from gologin import GoLogin
import threading
import time
import os
import traceback



class BrowserProfile:
    def __init__(self):
        self.browser=None
        self.goLoginApiToken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzU0Nzc2OWVkYTJiNTZiNDE4ZjkzOTciLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NzU0Nzc5N2E2YTNlMzg2NjE0ZjMwMmIifQ.9wnB_5fyYSOUnx_LefquxKunwSnId10GHJ1stMAtseo"

    def getGoLoginProfile(self,profileID):
        try:
            gl = GoLogin({
                'token': self.goLoginApiToken,
                'profile_id': profileID,
            })
            debugger_address = gl.start()
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", debugger_address)
            # path = chromedriver_autoinstaller.install(cwd=True)
            # print(path)
            #self.browser = webdriver.Chrome(executable_path=path, options=chrome_options)
            #self.browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
            return self.browser
        except Exception as e:
            print(traceback.format_exc())

    def getChromeInstanceProfile(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--window-size=1920,1080")
            # chrome_options.add_argument(
            #     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--profile-directory=Default")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-plugins-discovery")
            chrome_options.add_argument("--incognito")

            # chrome_options.add_argument("--start-minimized")
            # chrome_options.add_argument("--disable-extensions")
            # chrome_options.add_argument("--disable-popup-blocking")
            # chrome_options.add_argument("--profile-directory=Default")
            # chrome_options.add_argument("--ignore-certificate-errors")
            # chrome_options.add_argument("--disable-plugins-discovery")
            # chrome_options.add_argument("--incognito")

            # working
            # PROXY = "35.185.196.38:3128"
            # chrome_options.add_argument('--proxy-server=%s' % PROXY)
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

            th = threading.Thread(target=self.startChrome, args=())
            th.daemon = True
            th.start()

            time.sleep(3)
            #path = chromedriver_autoinstaller.install(cwd=True)
            #print(path)

            #self.browser = webdriver.Chrome(options=chrome_options)
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
            return self.browser
        except Exception as e:
            print(traceback.format_exc())

    def startChrome(self):
        return os.system('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')

    def closeAllChromeInstances(self):
        try:
            if self.browser is not None:
                self.browser.close()
                self.browser.quit()
            PROCNAME = "chromedriver.exe"
            userName = os.getlogin()
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME or proc.name() == 'chrome.exe':
                    if str(userName) in str(proc.username()):
                        print(str(proc.name()))
                        print(proc.username())
                        proc.kill()
        except Exception as ex:
            print(traceback.format_exc())
            
if __name__ == '__main__':


    browser=BrowserProfile()
    # driver=browser.getGoLoginProfile('6754776aeda2b56b418f9410')
    driver=browser.getChromeInstanceProfile()
    # driver = browser.startChrome()
    # browser.closeAllChromeInstances()


    time.sleep(5)
    driver.get('https://www.youtube.com/')