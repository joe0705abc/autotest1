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
save_dir = r"C:\Users\User\PycharmProjects\autotest1\Diabetes_page_content_3"
os.makedirs(save_dir, exist_ok=True)

count = 1

# 防止休眠
def prevent_sleep():
    while True:
        pyautogui.press("shift")
        print("已模擬 Shift 鍵，防止進入休眠")
        time.sleep(300)

threading.Thread(target=prevent_sleep, daemon=True).start()

# 點擊所有「查看更多」按鈕
def click_load_more_buttons(driver, wait):
    try:
        buttons = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "x1i10hfl") and contains(@class, "xjbqb8w") and contains(text(), "查看更多")]')
        ))
        for button in buttons:
            try:
                wait.until(EC.element_to_be_clickable(button))
                driver.execute_script("arguments[0].click();", button)
                print("成功點擊一個查看更多按鈕")
                time.sleep(3)
            except Exception as e:
                print(f"無法點擊查看更多按鈕: {e}")
    except Exception as e:
        print("找不到 '查看更多' 按鈕或已全部展開")

# 手動點擊查看更多＋滾動
def manual_expand_and_scroll(driver, wait):
    global count
    print("🔘 [F8] 點擊查看更多 + 滾動一次")
    print(f"🔄 第 {count} 輪開始")
    click_load_more_buttons(driver, wait)
    driver.execute_script("window.scrollBy(0, 1000);")
    print("⬇️ 頁面已滾動\n")
    count += 1

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

try:
    wait = login()
    print("🛑 請滾動到你要開始爬的日期附近")
    print("➡️ 按 F8：只點擊『查看更多』並滾動一次（用於手動探索）")
    print("➡️ 按 F9：開始自動爬蟲")

    # 等待 F9 或按 F8 多次
    while True:
        if keyboard.is_pressed("f9"):
            print("✅ 偵測到 F9，開始自動爬蟲流程")
            break
        elif keyboard.is_pressed("f8"):
            manual_expand_and_scroll(driver, wait)
            time.sleep(1)  # 防止重複偵測

    # 🧠 自動爬蟲主迴圈
    while True:
        count
        print(f"🔄 第 {count} 輪開始")
        click_load_more_buttons(driver, wait)

        raw_html = driver.page_source
        file_name = os.path.join(save_dir, f"facebook_page_{count}.html")
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(raw_html)
        print(f"✅ 第 {count} 次 HTML 已儲存：{file_name}")

        if count % 10 == 0:
            gc.collect()
            print("✅ 清除記憶體")

        driver.execute_script("window.scrollBy(0, 1000);")
        print("⬇️ 頁面已滾動\n")
        time.sleep(5)

        count += 1

except KeyboardInterrupt:
    print("❌ 手動中止程式。")
except Exception as e:
    print(f"⚠️ 發生錯誤: {e}")
finally:
    driver.quit()
