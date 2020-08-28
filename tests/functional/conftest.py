import pytest
from selenium import webdriver
from Consts import project_dir


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

def main_css():
    path = project_dir / "styles" / "index.css"
    with path.open("r") as src:
        yield src.read()