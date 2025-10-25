"""
main.py — Required Core: The Robot Driver
A Playwright-based Python script that logs into a demo website,
searches for a product, and reports its price.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import sys
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        print("Navigating to demo webstore...")
        page.goto("https://www.saucedemo.com", timeout=10000)

        print("Logging in...")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        page.wait_for_selector(".inventory_item", timeout=5000)
        print("Login successful!")

        print("Searching for product...")
        product_name = "Sauce Labs Backpack"
        item = page.locator(f"text={product_name}").first

        if item.count() == 0:
            raise Exception(f"Product '{product_name}' not found.")

        item.click()
        page.wait_for_selector(".inventory_details_price", timeout=5000)
        price = page.locator(".inventory_details_price").inner_text()

        print(f"Success! Product '{product_name}' found at price {price}")

    except PlaywrightTimeout:
        print("Error: Page took too long to load or element missing.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        time.sleep(2)
        browser.close()


if __name__ == "__main__":
    try:
        with sync_playwright() as playwright:
            run(playwright)
    except Exception as e:
        print(f"Critical failure: {e}")
        sys.exit(1)
