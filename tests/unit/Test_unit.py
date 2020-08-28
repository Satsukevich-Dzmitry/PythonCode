from path_create import build_path
from to_bytes import to_bytes
from path_create import get_contenttype
from custom_class import Endpoint


def test_normalize_path():
    dataset = {
        "": "/",
        "/": "/",
        "/hello": "hello/",
        "hello///": "hello///",
        "/hello": "/hello/",
    }

    for path, expected in dataset.items():
        got = build_path(path)
        assert got == expected,\
            f"path {path} normalized to {got},\
            while {expected} expected"


def test_encode():
    testing_data={
        b"12": b"12",
        "b": b"b",
    }
    for original, encoded in testing_data.items():
        result = to_bytes(original)
        assert result == encoded, \
            f"{original} didn't correctly turned into bytes"


def test_getting_filetype():
    dataset = {
        "unnamed.png": "png",
        "hello.css": "css",
        "index.html": "html",
    }
    for path, expected in dataset.items():
        got = get_contenttype(path)
        assert got == expected, \
            f"path {path} normalized to {got},\
                 while {expected} expected"

def test_endpoint():
    dataset = {
        "": Endpoint(original="", normal="/", file_name=None, query_string=None),
        "/": Endpoint(original="/", normal="/html_files/", file_name="index.html", query_string=None),
        "/images/unnamed.png/": Endpoint(original="/images/unnamed.png/", normal="/images/", file_name="unnamed.png", query_string=None),
        "/images/unnamed.png": Endpoint(original="/images/unnamed.png", normal="/images/", file_name="unnamed.png", query_string=None),
        "/images/unnamed.png/?wed": Endpoint(original="/images/unnamed.png/", normal="/images/", file_name="unnamed.png",
                                         query_string="wed"),
    }
    for path, expected in dataset.items():
        got = Endpoint.from_path(path)
        assert got == expected, f"Get {got}, while expected {expected}"
