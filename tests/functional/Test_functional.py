import pytest


@pytest.mark.functional
def test(chrome):
    chrome.get("http://localhost:8000/")
    assert "Opening_page(not_functional)" in chrome.title
    assert "unnamed" in chrome.page_source