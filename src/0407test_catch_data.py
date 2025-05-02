from bs4 import BeautifulSoup

# 讀取 HTML 檔案
with open('C:/Users/User/PycharmProjects/autotest1/Diabetes_page_content_1/facebook_page_17.html', 'r',
          encoding='utf-8') as file:
    html = file.read()

# 解析 HTML
soup = BeautifulSoup(html, 'lxml')

# 抓出所有貼文容器（非常精確）
posts = soup.select('div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
#x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z
already_seen_texts = set()

# 逐一處理每篇貼文
for i, post in enumerate(posts, 1):
    print(f"--- 貼文 {i} ---")

    # 發文者名稱
    poster = post.select_one(
        'span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs')
    print(" <發文者> ", poster.get_text(strip=True) if poster else "（無發文者）")

    #發文者URL
    a_tags = post.select(
        'a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xkrqix3.x1sur9pj.xzsf02u.x1s688f')
    for a in a_tags:
        href = a.get('href')
        print(" <發文者URL> ", href)

    # 發文時間
    time_anchor = post.select_one(
        'a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xkrqix3.x1sur9pj.xi81zsa.x1s688f'
    )

    if time_anchor:
        time_texts = []
        for span in time_anchor.find_all("span"):
            clean = span.get_text(strip=True).replace("-", "")
            if clean:
                time_texts.append(clean)
        final_time = ''.join(time_texts)
        print(" <發文時間> ", final_time if final_time else "（內容為空）")
    else:
        print(" <發文時間> （無找到時間區塊）")

    # 發文內容
    contents = post.select('div.html-div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd')
    if contents:
        print(" <文章內容> ")
        for content in contents:
            text = content.get_text(strip=True)
            if "-" in text or "facebook" in text.lower() or "回覆" in text or "查看更多回答" in text or text in already_seen_texts:
                continue
            if text:
                already_seen_texts.add(text)

                print(text)
    else:
        print("<無文字內容>")