from playwright.sync_api import Playwright, sync_playwright
import sys
import os

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    context.set_default_timeout(10000)
    page = context.new_page()
    page.goto('https://github.com/rebibabo/static_program_analysis_by_tree_sitter')
    page.locator('button.euQNNw').click()
    page.wait_for_timeout(100)
    with page.expect_download() as download_info:
        page.click('text=Download ZIP')
    download = download_info.value
    download.save_as(download.suggested_filename)
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)

