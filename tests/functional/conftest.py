import datetime
from functools import wraps

import pytest
from selenium import webdriver
from Consts import project_dir
from tests.functional.utils import build_chrome


@pytest.yield_fixture(scope="function", autouse=True)
def browser():
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


# @pytest.yield_fixture(scope="session", autouse=True)
# def browser():
#     br = build_chrome()
#     yield br
#     br.close()
#     br.quit()
#
#
# @pytest.yield_fixture(scope="session", autouse=True)
# def main_css():
#     path = project_dir / "styles" / "index.css"
#     with path.open("r") as src:
#         yield src.read()
