
import threading
import time
import sys
import os
import gc
import pyautogui
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# 設定程式輸出為 UTF-8

chrome_service = ChromeService()
chrome_options = ChromeOptions()
chrome_options.add_argument('--start-maximized')

# 啟動 ChromeDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Facebook 群組網址
url = "https://www.facebook.com/groups/diabetic99"

# 儲存路徑
save_dir = r"C:\Users\User\PycharmProjects\autotest1\Diabetes_page_content_3"
os.makedirs(save_dir, exist_ok=True)

count = 1
scrolling = False

# 防止休眠
def prevent_sleep():
    while True:
        pyautogui.press("shift")
        print("🛡️ 模擬 Shift 防止休眠")
        time.sleep(300)

threading.Thread(target=prevent_sleep, daemon=True).start()

# 自動滾動迴圈
def auto_scroll_loop():
    global scrolling
    while True:
        if scrolling:
            print("⬇️ 自動滾動中...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        else:
            time.sleep(0.2)
# 開始滾動執行緒
threading.Thread(target=auto_scroll_loop, daemon=True).start()

# 手動儲存 HTML 畫面
def save_html():
    global count
    raw_html = driver.page_source
    file_name = os.path.join(save_dir, f"facebook_page_{count}.html")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(raw_html)
    print(f"💾 HTML 已儲存：{file_name}")
    count += 1

# 登入 Facebook
def login():
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    input_account = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    input_password = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))
    input_account.send_keys("jncstafdn@outlook.co.nz")
    input_password.send_keys("mXk789l4CRl")
    input_password.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print("✅ 成功登入！")

try:
    login()

    print("🛠️ 操作說明：")
    print("➡️ 按 F7：開始滾動")
    print("➡️ 按 F8：停止滾動")
    print("➡️ 按 F9：儲存目前畫面 HTML")


    # 主迴圈 - 鍵盤控制
    while True:
        if keyboard.is_pressed("f7"):
            scrolling = True
            print("▶️ 已開始滾動")
            time.sleep(1)

        elif keyboard.is_pressed("f8"):
            scrolling = False
            print("⏸️ 已停止滾動")
            time.sleep(1)

        elif keyboard.is_pressed("f9"):
            save_html()


except KeyboardInterrupt:
    print("❌ 手動中止程式")
except Exception as e:
    print(f"⚠️ 發生錯誤：{e}")
finally:
    driver.quit()
