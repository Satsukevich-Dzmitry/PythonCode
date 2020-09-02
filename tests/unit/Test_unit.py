from web_app_namespace import Web_App_Names
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
        "": Request_http(method="get", original="", normal="/", contenttype="html", file_name=None, query_string=None),
        "/": Request_http(method="get", original="/", normal="/html_files/", contenttype="html", file_name="index.html", query_string=None),
        "/images/unnamed.png/": Request_http(method="get", original="/images/unnamed.png/", normal="/images/", contenttype="png", file_name= "unnamed.png", query_string=None),
        "/images/unnamed.png": Request_http(method="get", original="/images/unnamed.png", normal="/images/", contenttype="png", file_name="unnamed.png", query_string=None),
        "/images/unnamed.png/?wed": Request_http(method="get", original="/images/unnamed.png/", normal="/images/", contenttype="png", file_name="unnamed.png",
                                                 query_string="wed"),
    }
    for path, expected in dataset.items():
        got = Request_http.from_path(path, "get")
        assert got == expected, f"Get {got}, while expected {expected}"

def test_querystr_read():
    dataset = {
        "": Web_App_Names(name="stranger", surname="Didn't tell", age=0, year="Wrong Input"),
        "name=boy&surname=": Web_App_Names(name="boy", surname="Didn't tell", age=0, year="Wrong Input"),
        "name=boy&surname=test": Web_App_Names(name="boy", surname="test", age=0, year="Wrong Input"),
        "name=boy&surname=test&age=20": Web_App_Names(name="boy", surname="test", age=20, year="You was born at 2000"),
        "name=boy&surname=test&age=tt": Web_App_Names(name="boy", surname="test", age=0, year="Wrong Input"),
        "name=boy&surname=&age=tt": Web_App_Names(name="boy", surname="Didn't tell", age=0, year="Wrong Input"),
        "name=boy&surname=test&age=-20": Web_App_Names(name="boy", surname="test", age=0, year="Wrong Input"),
    }
    for qs, expected in dataset.items():
        got = Web_App_Names.get_qs_info(qs)
        assert got == expected, f"With {qs} get {got}, while expected {expected}"
