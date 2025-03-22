import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#API KEY- you need to get your own API key from OpenAI
OPENAI_API_KEY = ""

# OpenAI API
openai.api_key = OPENAI_API_KEY
chrome_driver_path = r"C:\Users\The user\Downloads\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

#open the browser
driver = webdriver.Chrome(service=service)

#open whatsapp
driver.get("https://web.whatsapp.com")
input("click enter ")


def open_chat(phone_number):
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}"
    driver.get(whatsapp_url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
    )

def get_last_message():
    try:
        #to find the last message
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]"))
        )

        messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]")
        if messages:
            last_message = messages[-1].text.strip()  #the last message
            print(f"the last message is {last_message}")
            return last_message
        else:
            print("no messages")
            return None

    except Exception as e:
        driver.save_screenshot("error_screenshot.png")  
        print("error")
        return None


def send_message(message):
    try:
        #send the message
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
        )
        input_box.click()
        time.sleep(1)
        input_box.send_keys(message)
        time.sleep(2)
        input_box.send_keys(Keys.ENTER)
        print("the message was sent")
    except Exception as e:
        driver.save_screenshot("error_screenshot.png")

#ask the GPT-3
def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


fone_numbers=[""]
last_seen_messages = {num: None for num in fone_numbers} 

while True:
    for phone_number in fone_numbers:
        open_chat(phone_number)  
        time.sleep(3)  

        current_message = get_last_message()

        if current_message and current_message != last_seen_messages[phone_number]:#if there is a new message
            last_seen_messages[phone_number] = current_message  

            #the answer from the GPT-3
            gpt_reply = ask_gpt(current_message)
            send_message(gpt_reply) #send the answer

    time.sleep(20)  # wait 20 seconds before checking again