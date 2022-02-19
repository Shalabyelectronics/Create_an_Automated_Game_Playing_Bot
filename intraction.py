from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

CHROMEDRIVER = os.environ.get("CHROMEDRIVER")
Service(executable_path=CHROMEDRIVER)
driver = webdriver.Chrome()
driver.get("http://orteil.dashnet.org/experiments/cookie/")


def cookies_game():
    # ToDo First Find cookie by ID
    cookies = driver.find_element(By.ID, "cookie")
    # ToDo Get upgrade item Id'
    upgrade_items = [item.get_attribute("id") for item in driver.find_elements(By.CSS_SELECTOR, "#store div")
                     if item.get_attribute("id") != "buyElder Pledge"]
    # ToDo Create timeout varable that would check for upgrade items each five seconds and the code will loop for 5 min.
    timeout = time.time() + 5
    five_minutes = time.time() + 60 * 1
    while True:
        cookies.click()
        # Now I want to write a condition that check every 5 seconds for the prices and if we have enough money.
        if time.time() > timeout:
            items_prices = [
                int(driver.find_element(By.XPATH, f"//div[@id='{item}']/b").text.split()[-1].strip().replace(",", ""))
                for item in upgrade_items]
            store = {price: item for price, item in zip(items_prices, upgrade_items)}
            cookies_count = int(driver.find_element(By.ID, "money").text.strip().replace(",", ""))
            affordable_items = {}
            for price, item in store.items():
                if cookies_count > price:
                    affordable_items[price] = item

            affordable_item = affordable_items[max(affordable_items)]
            item = driver.find_element(By.ID, affordable_item)
            item.click()

            timeout = time.time() + 5

        if time.time() > five_minutes:
            cookies_per_click = driver.find_element(By.ID, "cps").text
            print(cookies_per_click)
            break


cookies_game()
