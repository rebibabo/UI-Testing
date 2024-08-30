from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import os
p = lambda p : p.replace("\xa0", " ")

# 安装
# pip install pytest-playwright
# playwright install

# 官网注册账号
KEY = 'RAG'     # 关键词
NAME = '19891771663'   # 用户名   
PASSWORD = '82947535yzs'   # 密码

def download(url, path):
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)

def run(playwright: Playwright) -> None:
    if not os.path.exists(KEY):
        os.makedirs(KEY)
    print("登陆中...")
    browser = playwright.chromium.launch(headless=False)    # 如果不想打开网页，设置为True
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.patentstar.com.cn/")
    page.get_by_text("登录").click()
    page.locator("#loginname").click()
    page.locator("#loginname").fill(NAME)
    page.locator("#password").click()
    page.locator("#password").fill(PASSWORD)
    page.get_by_role("button", name="登录").click()
    print("登陆成功")
    page.get_by_placeholder("请输入关键词").click()
    page.get_by_placeholder("请输入关键词").press("CapsLock")
    page.get_by_placeholder("请输入关键词").fill(KEY)
    page.get_by_placeholder("请输入关键词").press("CapsLock")
    page.get_by_text("检索", exact=True).click()
    page_num = int(page.locator(".tcdNumber").last.inner_text())
    next_bnt = page.locator(".nextPage")
    page.wait_for_timeout(2000)
    for _ in range(page_num):
        try:
            lcs = page.locator("#listcontainer > div").all()
            for lc in lcs:
                url = lc.locator(".title-color")
                name = url.inner_text()
                print(name)
                process = lc.locator("p.fl").inner_text()
                info = lc.locator(".p2 p").all_inner_texts()
                summary = lc.locator(".p3").inner_text()
                if not os.path.exists(f"{KEY}/{name}"):
                    os.makedirs(f"{KEY}/{name}")
                elif os.path.exists(f"{KEY}/{name}/1.pdf"):
                    continue
                with open(f"{KEY}/{name}/info.txt", "w", encoding='utf-8') as f:
                    f.write(f"名称：{name}\n")
                    f.write(f"进度：{p(process)}\n")
                    for i in info:
                        f.write(f"{p(i)}\n")
                    f.write(f"{p(summary)}\n")
                pic_url = lc.locator(".t2 a").get_attribute("href")
                url.click()
                page.wait_for_timeout(3000)
                page1 = context.pages[-1]
                page1.locator("#itemPdf").click()
                pdf_url = page1.locator("embed").get_attribute("src")
                download(pdf_url, f"{KEY}/{name}/1.pdf")
                download(pic_url, f"{KEY}/{name}/1.jpg")
                page1.close()
                page.bring_to_front()
        except Exception as e:
            print("error")
            print(e)
            for page in context.pages[1:]:
                page.close()
        next_bnt.click()
        page.wait_for_timeout(1000)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)