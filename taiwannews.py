# import requests
# from bs4 import BeautifulSoup
# import time
# import os
# import csv
# import random

# # ===== 1. 增強 Headers =====
# # 加入 Referer 和更完整的瀏覽器特徵
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
#     "Referer": "https://www.taiwannews.com.tw/en/index", # 模擬從首頁進入
#     "Connection": "keep-alive"
# }

# data = []

# # ===== 2. 開始爬取 =====
# for page in range(1, 11):
#     # 目前 Taiwan News 的政治分類標準分頁網址
#     url = f"https://www.taiwannews.com.tw/en/list/politics?page={page}"
#     print(f"\n🚀 正在抓取第 {page} 頁: {url}")

#     try:
#         res = requests.get(url, headers=headers, timeout=15)
        
#         if res.status_code != 200:
#             print(f"  ❌ 無法存取，狀態碼: {res.status_code}。可能是觸發了 WAF 封鎖。")
#             continue

#         res.encoding = "utf-8"
#         soup = BeautifulSoup(res.text, "html.parser")
        
#         # 修改選擇器：Taiwan News 目前文章區塊多用 .list-item 或直接在 <a> 標籤內
#         # 我們抓取包含標題字樣的連結，並排除掉分頁與分類連結
#         articles = soup.find_all('a', href=True)
        
#         found_count = 0
#         for a_tag in articles:
#             href = a_tag.get("href")
#             title = a_tag.text.strip()
            
#             # 關鍵過濾條件：通常文章連結長度較長，且不包含 /list/ 或 /category/
#             if "/en/news/" in href and len(title) > 10:
#                 link = href if href.startswith("http") else "https://www.taiwannews.com.tw" + href

#                 # 避免重複抓取同一篇
#                 if any(d['連結'] == link for d in data):
#                     continue

#                 print(f"  📝 處理: {title[:15]}...")

#                 try:
#                     # 抓取內文前，隨機休息 1~3 秒，避免頻率太快
#                     time.sleep(random.uniform(1, 3))
                    
#                     art_res = requests.get(link, headers=headers, timeout=10)
#                     art_soup = BeautifulSoup(art_res.text, "html.parser")
                    
#                     # 針對最新版內文標籤進行多樣匹配
#                     content_tag = art_soup.select_one("div.article-content, div.article-body, article, .p-content")
#                     if content_tag:
#                         # 移除廣告或不必要的腳注（選填）
#                         content = content_tag.get_text(separator=' ', strip=True)
#                     else:
#                         content = "（內容擷取失敗）"
                    
#                     date_tag = art_soup.select_one("time, .date, .p-time, span.text-muted")
#                     date = date_tag.text.strip() if date_tag else "無日期"
                    
#                     data.append({
#                         "標題": title,
#                         "日期": date,
#                         "連結": link,
#                         "內文": content
#                     })
#                     found_count += 1
#                 except Exception as e:
#                     print(f"    ⚠️ 內文抓取失敗: {link[:30]}... 錯誤: {e}")
#                     continue

#         print(f"  ✅ 第 {page} 頁完成，目前累計 {len(data)} 篇")
        
#         # 換頁時大休一下，模擬人類翻頁行為
#         time.sleep(random.uniform(3, 5))

#     except Exception as e:
#         print(f"❌ 嚴重錯誤: {e}")

# # ===== 3. 存檔 =====
# file_name = "taiwan_news_politics_v2.csv"

# if data:
#     with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
#         writer = csv.DictWriter(f, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
#     print(f"\n🎉 成功！共抓到 {len(data)} 筆資料，已存入 {file_name}。")
# else:
#     print("\n😱 依然沒抓到資料。可能原因：")
#     print("1. 網站完全擋掉非瀏覽器的 Request (這時只能用 Selenium)")
#     print("2. 網頁選擇器 (Selector) 需要根據當下網頁原始碼手動微調")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# 1. 設置瀏覽器參數
chrome_options = Options()
# chrome_options.add_argument('--headless') # 如果不想看到視窗彈出，可以取消這行註解
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# 2. 啟動瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)

data = []

try:
    # 抓取前 3 頁政治新聞
    for page in range(1, 4):
        url = f"https://www.taiwannews.com.tw/en/list/politics?page={page}"
        print(f"🌐 正在爬取第 {page} 頁...")
        driver.get(url)
        
        driver.save_screenshot("check_error.png")
        
        # 等待新聞列表出現
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/en/news/']")))
        
        # 取得頁面上所有新聞連結
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/news/']")
        
        # 整理出有效的文章清單（過濾重複與短標題）
        urls = []
        for link in links:
            href = link.get_attribute('href')
            title = link.text.strip()
            if href and len(title) > 15 and href not in [u['link'] for u in urls]:
                urls.append({'title': title, 'link': href})

        # 逐一進入文章抓取內文
        for item in urls:
            print(f"  📝 讀取文章: {item['title'][:15]}...")
            driver.get(item['link'])
            
            try:
                # 抓取日期
                date = driver.find_element(By.CSS_SELECTOR, "time, .p-time").text.strip()
                # 抓取內文（針對不同標籤做嘗試）
                content_box = driver.find_element(By.CSS_SELECTOR, "div.article-content, article, .p-content")
                content = content_box.text.replace('\n', ' ').strip()
                
                data.append({
                    "標題": item['title'],
                    "日期": date,
                    "連結": item['link'],
                    "內文": content
                })
            except:
                print(f"    ⚠️ 文章 {item['title'][:10]} 抓取內容失敗")
            
            time.sleep(1) # 休息一下，避免太頻繁
            driver.back() # 回到列表頁

    # 3. 儲存結果
    with open('taiwan_news_politics.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["標題", "日期", "連結", "內文"])
        writer.writeheader()
        writer.writerows(data)
    print(f"\n🎉 任務完成！共抓取 {len(data)} 筆新聞。")

finally:
    driver.quit()