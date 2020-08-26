import pytest


@pytest.mark.functional
def test(firefox):
    firefox.get("http://localhost:8000/")
    assert "Opening_page" in firefox.title
    assert "/images/opening_picture.jpg/" in firefox.page_source
