from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(snapshots=True, sources=True, screenshots=True)
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("nihao")
    page.locator("#kw").press("Enter")
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)