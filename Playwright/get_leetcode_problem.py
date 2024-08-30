from playwright.sync_api import Playwright, sync_playwright, expect

# CSS元素选择子
# class="animal" -> .animal
# class="animal plant" -> .animal.plant
# id="unique" -> #unique
# <div> -> div
# href="www" -> [href="www"] 或者不指定其值[href]

# 多级选择器
# div > a -> div下的a，a是直接子元素，这里的div也可以是class或id
# div a -> div下的所有a，a是子孙元素

# 模糊匹配
# [href*=www] -> href属性包含www的元素
# [href^=www] -> href属性以www开头的元素
# [href$=www] -> href属性以www结尾的元素

def run(playwright: Playwright, n: int, language: str) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page_index = (n-1) // 50 + 1
    problem_index = (n-1) % 50 + 1
    page.goto(f"https://leetcode.cn/problemset/?page={page_index}")
    page.wait_for_timeout(5000)
    lcs = page.locator(".truncate .h-5")
    problem_page = f'https://leetcode.cn/{lcs.nth(problem_index - 1 + int(page_index == 1)).get_attribute("href")}/description'
    page.goto(problem_page)
    page.wait_for_timeout(10000)
    page.locator(".popover-wrapper button.rounded").last.click()
    lcs = page.locator(".text-text-primary.text-sm").all()
    for lc in lcs:
        if lc.inner_text() == language:
            lc.click()
            break
    page.wait_for_timeout(1000)
    lcs = page.locator('.view-lines[role="presentation"]').first
    print(lcs.inner_text())
    context.close()
    browser.close()

with sync_playwright() as playwright:
    lang_map = {0:"C++", 1:"Java", 2:"Python", 3:"Python3", 4:"C", 5:"C#", 6:"JavaScript", 7:"TypeScript", 8:"PHP", 9:"Swift", 10:"Kotlin", 11:"Dart", 12:"Go", 13:"Ruby", 14:"Scala", 15:"Rust", 16:"Racket", 17:"Erlang", 18:"Elixir"}
    index = int(input("The problem index: \n>>> "))
    for k, v in lang_map.items():
        print(f"({k}: {v})", end=" ")
    language = lang_map[int(input("\nThe language index: \n>>> "))]
    run(playwright, index, language)

