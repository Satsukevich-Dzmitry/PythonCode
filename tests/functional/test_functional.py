from datetime import date

import pytest
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.functional.pages import hellopage
from tests.functional.pages.hellopage import HelloPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from tests.functional.utils import screenshot_on_failure

url = "http://localhost:8000"
urlhello = "http://localhost:8000/hello/"
"""
@pytest.mark.functional
def test_opening_page(firefox):
    firefox.get(url)
    assert "Opening_page" in firefox.title
    assert "/images/opening_picture.jpg/" in firefox.page_source
    assert "/style/index.css/" in firefox.page_source

@pytest.mark.functional
def test_styles(firefox, main_css):
    firefox.get(f"{url}/style/index.css")
    assert main_css in firefox.page_source
"""
@pytest.mark.functional
@screenshot_on_failure
def test_hello(browser, request):
    name = "Dima"
    surname = "Sat"
    age = 19
    year = date.today().year - age

    page = HelloPage(browser, urlhello)

    anon_on_page = "stranger none!"
    name_and_surname_on_page = f"Hello {name} {surname}!"
    year_on_page = f"You was born at {year}!"

    validate_content(page, anon_on_page)

    set_input_name_value(page, name)
    set_input_surname(page, surname)
    set_input_age_value(page, age)
    submit(page)
    validate_redirect(page, fr"hello/?")
    validate_content(page, name_and_surname_on_page, year_on_page)


def set_input_name_value(page: HelloPage, value: str):
    page.input_name.clear()
    if value:
        page.input_name.send_keys(value)


def set_input_surname(page: HelloPage, value: str):
    page.input_surname.clear()
    if value:
        page.input_surname.send_keys(value)


def set_input_age_value(page: HelloPage, value: int):
    page.input_age.clear()
    if value:
        page.input_age.send_keys(value)


def submit(page: HelloPage):
    page.button_greet.send_keys(Keys.RETURN)


def validate_content(page: HelloPage, *texts):
    html = page.html

    for text in texts:
        assert text in html


def validate_redirect(page: HelloPage, url: str):
    try:
        redirected = WebDriverWait(page.browser, 4).until(
            expected_conditions.url_matches(url)
        )
        assert redirected
    except TimeoutException as err:
        raise AssertionError("no redirect") from err
