import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#API KEY
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


def open_chat(chat_name):
    try:
        print(f"search for a grop with the name {chat_name}")

        
        sidebar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))
        )

        chats = sidebar.find_elements(By.XPATH, ".//span[@title]")
        for chat in chats:
            title = chat.get_attribute("title").strip()
            if chat_name in title:
                chat.click()
                time.sleep(2)
                return

        print(f"chat with the name {chat_name} not found")
        

    except Exception as e:
        print("error in open chat")
        

def get_last_message():
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]"))
        )
        messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]")
        if messages:
            last_message = messages[-1].text.strip()
            print(f"the last message is: {last_message}")
            return last_message
        else:
            print("no messages found")
            return None
    except Exception as e:
        print("error in get_last_message")
        return None


def send_message(message):
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
        )
        input_box.click()
        time.sleep(1)
        input_box.send_keys(message)
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)
        print("message sent")
    except Exception as e:
        print("error in send_message")
       


def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("error in ask_gpt")
        return None


group_names = ['']



last_seen_messages = {group: None for group in group_names}


while True:
    for group in group_names:
        open_chat(group)
        time.sleep(3)

        current_message = get_last_message()

        if current_message and current_message != last_seen_messages[group]:
            last_seen_messages[group] = current_message
            gpt_reply = ask_gpt(current_message)
            send_message(gpt_reply)

    time.sleep(10)
