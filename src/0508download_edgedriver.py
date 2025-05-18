import threading
import time
import sys
import os
import gc

import pyautogui
import keyboard
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# 設定程式輸出為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 設定 Edge WebDriver
edge_options = EdgeOptions()
edge_options.add_argument('--start-maximized')
edge_service = EdgeService()
driver = webdriver.Edge(service=edge_service, options=edge_options)

# Facebook 群組網址
url = "https://www.facebook.com/groups/diabetic99"

# 儲存路徑
save_dir = r"C:\Users\User\PycharmProjects\autotest1\Diabetes_page_content_4"
os.makedirs(save_dir, exist_ok=True)

count = 1

# 防止休眠
def prevent_sleep():
    while True:
        pyautogui.press("shift")
        print("已模擬 Shift 鍵，防止進入休眠")
        time.sleep(300)

threading.Thread(target=prevent_sleep, daemon=True).start()


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
    return wait

def download_file(raw_html):
    global count
    file_name = os.path.join(save_dir, f"facebook_page_{count}.html")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(raw_html)
    print(f"✅ 第 {count} 次 HTML 已儲存：{file_name}")
    count += 1


try:
    wait = login()
    print("🛑 請滾動到你要開始爬的日期附近")
    print("➡️ 按 f9：下載")




    # 🧠 自動爬蟲主迴圈
    while True:
        while keyboard.is_pressed("f9"):
            print("✅ 偵測到 f9，開始下載")
            raw_html = driver.page_source
            download_file(raw_html)




except KeyboardInterrupt:
    print("❌ 手動中止程式。")
except Exception as e:
    print(f"⚠️ 發生錯誤: {e}")
finally:
    driver.quit()
