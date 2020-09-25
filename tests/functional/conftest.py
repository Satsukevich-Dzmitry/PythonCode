import datetime
from functools import wraps

import pytest
from selenium import webdriver
from Consts import project_dir
from tests.functional.utils import build_chrome

"""
@pytest.yield_fixture(scope="function", autouse=True)
def firefox():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--redirect")

    browser = webdriver.Firefox(options=firefox_options)
    browser.implicitly_wait(10)

    try:
        yield browser
    finally:
        browser.close()
        browser.quit()


@pytest.yield_fixture(scope="function", autouse=True)
def main_css():
    path = project_dir / "styles" / "index.css"
    with path.open("r") as src:
        yield src.read()
"""

@pytest.yield_fixture(scope="session", autouse=True)
def browser():
    chrome = build_chrome()
    yield chrome
    chrome.close()
    chrome.quit()


@pytest.yield_fixture(scope="session", autouse=True)
def main_css():
    path = project_dir / "styles" / "index.css"
    with path.open("r") as src:
        yield src.read()
