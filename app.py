"""This python file will do the AutoClass job."""
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()

options = webdriver.ChromeOptions()
if config.get("headless"):
    options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


def driver_send_keys(locator, key):
    """Send keys to element.

    :param locator: Locator of element.
    :param key: Keys to send.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    """Click element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def driver_screenshot(locator, path):
    """Take screenshot of element.

    :param locator: Locator of element.
    :param path: Path to save screenshot.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).screenshot(path)


def driver_get_text(locator):
    """Get text of element.

    :param locator: Locator of element.
    :return: Text of element.
    """
    return WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).text


def login():
    """Login to FJU Tronclass."""
    driver.get('https://caselearn2.fju.edu.tw/cas/login?service=https://elearn2.fju.edu.tw/login&locale=zh_TW')
    driver_send_keys((By.ID, "username"), config.get("username"))
    driver_send_keys((By.ID, "password"), config.get("password"))
    driver_screenshot((By.XPATH, "/html/body/div/div/div/div[1]/div/form/section[3]/img"), "captcha.png")
    driver_send_keys((By.ID, "captcha"), utils.get_ocr_answer("captcha.png"))
    driver_click((By.XPATH, "/html/body/div/div/div/div[1]/div/form/section[4]/input[4]"))
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located((By.ID, "userCurrentName")))
    except TimeoutException:
        print("Login Failed, relog now.")
        login()
    print('-------------------------------------')
    print("Login Success!")


if __name__ == "__main__":
    login()
    time.sleep(10000)
    print('Time out, quit.')
    driver.quit()
