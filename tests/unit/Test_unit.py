
from custom_func import build_path, to_bytes
from custom_func import get_contenttype
from custom_class import Request_http


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
        "hellodark.css": "css",
        "index.html": "html",
    }
    for path, expected in dataset.items():
        got = get_contenttype(path)
        assert got == expected, \
            f"path {path} normalized to {got},\
                 while {expected} expected"

def test_endpoint():
    dataset = {
        "": Request_http(method="get", original="", normal="/", contenttype="html", file_name=None, query_string=None),
        "/": Request_http(method="get", original="/", normal="/html_files/", contenttype="html", file_name="index.html", query_string=None),
        "/images/unnamed.png/": Request_http(method="get", original="/images/unnamed.png/", normal="/images/", contenttype="png", file_name= "unnamed.png", query_string=None),
        "/images/unnamed.png": Request_http(method="get", original="/images/unnamed.png", normal="/images/", contenttype="png", file_name="unnamed.png", query_string=None),
        #"/images/unnamed.png/?wed": Request_http(method="get", original="/images/unnamed.png/", normal="/images/", contenttype="png", file_name="unnamed.png",
         #                                        query_string="wed"),
    }
    for path, expected in dataset.items():
        got = Request_http.from_path(path, "get")
        assert got == expected, f"Get {got}, while expected {expected}"


