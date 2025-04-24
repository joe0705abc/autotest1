import time
import sys
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
url = "https://www.facebook.com/adidasTW/?brand_redir=182162001806727"

try:
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # 登錄
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
        time.sleep(5)  # 等待內容載入

        # **獲取並整理 HTML**
        raw_html = driver.page_source
        soup = BeautifulSoup(raw_html, "html.parser")
        formatted_html = soup.prettify()  # 美化 HTML

        # **儲存格式化後的 HTML 檔案**
        file_name = f"facebook_page_{count}.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(formatted_html)
        print(f"第 {count} 次 HTML 下載並格式化完成！儲存為 '{file_name}'")

        # **使用 JavaScript 滾動到底部**
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"第 {count} 次滾動到底部")

        count += 1  # 遞增計數器
        time.sleep(5)  # 等待新內容載入

except KeyboardInterrupt:
    print("手動中止程式。")
except Exception as e:
    print(f"發生錯誤: {e}")
finally:
    driver.quit()
