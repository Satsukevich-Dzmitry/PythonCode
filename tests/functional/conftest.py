import pytest
from selenium import webdriver


@pytest.yield_fixture(scope="function", autouse=True)
def firefox():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")

    browser = webdriver.Firefox(firefox_options=firefox_options)
    browser.implicitly_wait(10)

    try:
        yield browser
    finally:
        browser.close()
        browser.quit()
