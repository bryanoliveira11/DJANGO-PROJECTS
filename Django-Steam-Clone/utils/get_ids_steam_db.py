from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def make_google_browser(headless=False, *options):
    DRIVER_PATH = Path(__file__).parent / 'driver' / 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_service = Service(
        executable_path=str(DRIVER_PATH),
    )

    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options,
    )

    return browser


def get_ids():
    browser = make_google_browser()
    browser.get('https://steamdb.info/charts/')
    table = browser.find_element(By.ID, 'table-apps')
    elements = table.find_elements(By.CLASS_NAME, 'app')
    ids_list = []
    for element in elements:
        ids_list.append(element.get_attribute('data-appid'))

    return ids_list
