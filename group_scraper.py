from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gologin import GoLogin
from webdriver_manager.chrome import ChromeDriverManager
import csv
from go_login import BrowserProfile

import random 
import os
import time
from sys import platform

from dotenv import load_dotenv
load_dotenv()

username = os.getenv('username')
password = os.getenv('password')



# # Set up the Firefox options
# options = Options()
# service = Service(ChromeDriverManager().install())
# # options.add_argument("--headless")
# # driver = webdriver.Firefox( options=options )
# # driver = webdriver.Chrome( options=options )



def open_profile():
    gl = GoLogin({
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NzRjNjdiODZmYTRjZWVjM2FhMWI0ZWYiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NzRkNDAzMTY5ZjMzNTA2NDE1MzZmODIifQ.S8QUkxmXKvT2pGPoFSRR2Sogxb22KdKQza6GX-fbuA8',
        'profile_id': '674c67b96fa4ceec3aa1b568'
    })
    debugger_address = gl.start()


    # if platform == "linux" or platform == "linux2":
	#     chrome_driver_path = "./chromedriver"
    # elif platform == "darwin":
    #     chrome_driver_path = "./mac/chromedriver"
    # elif platform == "win32":
    #     chrome_driver_path = "chromedriver.exe"


    options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome( options=options )   

    driver.get("https://www.facebook.com/")
    assert "Python" in driver.title
    driver.close()
    time.sleep(3)
    gl.stop()


def login(username, password):  


    try:
        # Open Facebook login page
        driver.get("https://www.facebook.com/")
        time.sleep(3)  # Allow time for the page to load

        # Locate the username and password fields
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "pass")

        # Input credentials
        email_field.send_keys(username)
        password_field.send_keys(password)

        # Submit login form
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Allow time to log in

        #refuse save popup
        try:
            time.sleep(5)
            save_button = driver.find_elements(By.XPATH, "//div[(@aria-label='Save') and (@role='button')]")
            save_button[0].click()

            print("Refuse button clicked")

        except Exception as e:  
            print(f"No dialogue box found {e}")

    except Exception as e:
        print(f"Error: {e}")

def confirm_friends_request():
    print("Confirming friends request ... ")
    time.sleep(5)
    driver.get("https://www.facebook.com/friends/requests")

    # Wait for the page to load
    time.sleep(15)
    try:
        # Find and click the "Confirm" button
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='screen-root']/div/div/div/div[4]")))
        print("Founding Confirm button")
        friends_list = driver.find_elements(By.XPATH, "//div[@data-visualcompletion='ignore-dynamic']/a")
        print(len(friends_list))

        for friend in friends_list:
            confirm_button = friend.find_element(By.XPATH, "./div[1]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/span/span")
            confirm_button.click()

            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 300);")

    except Exception as e:
        print(f"Error: {e}")    

def get_group_members(group_url):
    print("Group scraping ... ")
    try: 
        driver.get(group_url)

        time.sleep(10)    
        data = [["Name", "Profile ID"]] 

 
        # driver.find_element(By.TAG_NAME, "body").click()
        driver.execute_script("window.scrollTo(0, 8000);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 8000);")

        members_list = driver.find_elements(By.XPATH, "//div[@role='listitem' and @data-visualcompletion='ignore-dynamic']")
        print(len(members_list))

        for member in members_list:
            print('Inner for loop')
            member_data = member.find_element(By.XPATH, "./div/div/div[2]/div[1]/div/div/div[1]/span/span[1]/span/a")
            member_name = member_data.text
            print(member_name)

            # Get the 'href' attribute
            member_link = member_data.get_dom_attribute("href")
            print(member_link)
            member_id = member_link.split("/")[-2]
            print(member_id)
            data.append([member_name, member_id])

            time.sleep(1)

        # Save to CSV
        with open("scraped_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print("Scraped data saved to scraped_data.csv")


    except Exception as e:
        print(f"Error: {e}")

def send_message(message):
    print("Sending message ... ")

    #read profile links from csv
    with open("scraped_data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)

    driver.get("https://www.facebook.com/")
    time.sleep(5)

    for i in range(1, len(data)):
        name = data[i][0]
        profile_id = data[i][1]

        print(f'Sending message to {name}')
        driver.get(f'https://www.facebook.com/{profile_id}')

        time.sleep(random.randint(5, 10))    

        try:
            message_button = driver.find_element(By.XPATH, "//span[text()='Message']")
            message_button.click()

            time.sleep(1)

            message_text_box = driver.find_element(By.XPATH, f"//div[@aria-describedby='Write to {name}']")
            message_text_box.click()

            message_text_box.send_keys(message)
            message_text_box.send_keys(Keys.ENTER)
  
            time.sleep(5)

            close_chat_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Close chat']")
            for button in close_chat_buttons:
                button.click()

        except Exception as e:
            print(f"Error: {e}")



#####################
# open_profile()

browser=BrowserProfile()
browser.closeAllChromeInstances()
# driver=browser.getGoLoginProfile('6754776aeda2b56b418f9410')
driver=browser.getChromeInstanceProfile()
# driver = browser.startChrome()



# login(username, password)
# confirm_friends_request()

group_id = 'upworkersgroup'
group_url = f"https://www.facebook.com/groups/{group_id}/members"
# get_group_members(group_url)

message = 'Hi, '
send_message(message)
