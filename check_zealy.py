from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://zealy.io/cw/bastard/questboard", wait_until="networkidle")

    print(page.title())
    print(page.locator("body").inner_text()[:5000])

    browser.close()
