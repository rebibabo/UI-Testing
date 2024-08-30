from playwright.sync_api import Playwright, sync_playwright, expect
import re

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://fanyi.youdao.com/") 
    page.locator("div").filter(has_text=re.compile(r"^翻译$")).click()
    page.locator(".ic_language_arrowdown").first.click()
    page.get_by_text("英语").first.click()
    page.locator("#js_fanyi_input").click()
    page.wait_for_timeout(1000)
    while True:
        word = input("=" * 100 + "\n>>> ")
        page.locator("#js_fanyi_input").click()
        page.locator("#js_fanyi_input").fill(word)
        page.wait_for_timeout(1000)
        if page.locator(".pron").count():   # 单个单词，打印音标以及所有意思
            for text in page.locator(".pron").all_inner_texts():
                split = text.split()
                if not split:
                    continue
                else:
                    print(f"{split[0]}: /{split[1]}/")
            print(page.locator(".paraphrase-container").first.inner_text())
        else:   # 句子，直接显示翻译
            print(page.locator(".tgt.un-step-trans").inner_text())

with sync_playwright() as playwright:
    run(playwright)