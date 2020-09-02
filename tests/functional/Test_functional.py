import pytest


url = "http://localhost:8000"

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

@pytest.mark.functional
def test_query_string(firefox):
    firefox.get(f"{url}/hello/?name=Name&surname=Surname&age=11")
    assert "Name", "Surname" in firefox.page_source
    assert "2009" in firefox.page_source
