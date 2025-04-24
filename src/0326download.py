import threading
import time
import sys
import os  # 新增 os 模組

import pyautogui
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup  # 新增 BeautifulSoup

# 設定程式輸出為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 設定 Edge WebDriver
edge_options = EdgeOptions()
edge_options.add_argument('--start-maximized')
edge_service = EdgeService()

# 開啟 Edge 瀏覽器
driver = webdriver.Edge(service=edge_service, options=edge_options)

# Facebook 群組網址
url = "https://www.facebook.com/groups/diabetic99"

# 設定儲存目錄
save_dir = r"../Diabetes_page_content"
os.makedirs(save_dir, exist_ok=True)  # 若目錄不存在則建立

def prevent_sleep():
    while True:
        pyautogui.press("shift")  # 模擬按一下 Shift 鍵
        print("已模擬 Shift 鍵，防止進入休眠")
        time.sleep(300)  # 每 5 分鐘執行一次
sleep_thread = threading.Thread(target=prevent_sleep, daemon=True)
sleep_thread.start()
def click_load_more_buttons(driver, wait):
    """
    點擊所有 '查看更多' 按鈕
    """
    try:
        # 查找 '查看更多' 按鈕
        buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "x1i10hfl") and contains(@class, "xjbqb8w") and contains(text(), "查看更多")]')))
        for button in buttons:
            try:
                # 確保按鈕可點擊
                wait.until(EC.element_to_be_clickable(button))
                driver.execute_script("arguments[0].click();", button)
                print("成功點擊一個查看更多按鈕")
                time.sleep(3)  # 點擊後等待新內容加載
            except Exception as e:
                print(f"無法點擊查看更多按鈕: {e}")
    except Exception as e:
        print("找不到 '查看更多' 按鈕或已全部展開")


try:
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # 登錄 Facebook
    input_account = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
    input_password = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))
    input_account.send_keys("jncstafdn@outlook.co.nz")
    input_password.send_keys("mXk789l4CRl")
    input_password.send_keys(Keys.RETURN)

    # 等待頁面載入完成
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print("成功登入！")

    count = 1  # 計算下載次數
    while True:
        # 滾動頁面
        driver.execute_script(f"window.scrollBy(0, 1000);")
        print(f"第 {count} 次滾動")
        time.sleep(5)  # 滾動後等待頁面加載

        # 點擊 '查看更多' 按鈕
        click_load_more_buttons(driver, wait)
        raw_html = driver.page_source
        soup = BeautifulSoup(raw_html, "html.parser")
        formatted_html = soup.prettify()  # 美化 HTML

        # **儲存格式化後的 HTML 檔案**
        file_name = os.path.join(save_dir, f"facebook_page_{count}.html")
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(formatted_html)
        print(f"第 {count} 次 HTML 下載並格式化完成！儲存為 '{file_name}'")

        count += 1

        # 每次滾動後再次給予時間讓頁面穩定
        time.sleep(5)

except KeyboardInterrupt:
    print("手動中止程式。")
except Exception as e:
    print(f"發生錯誤: {e}")
finally:
    driver.quit()
