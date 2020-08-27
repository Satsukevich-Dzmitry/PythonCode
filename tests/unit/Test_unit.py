from path_create import build_path
from to_bytes import to_bytes
from path_create import get_file_for_path
from path_create import get_contenttype


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

def test_getting_path():
    dataset = {
        "/": ("/html_files/", "index.html"),
        "/html_files/hello.html": ("/html_files/", "hello.html"),
        "/images/unnamed.png/": ("/images/", "unnamed.png"),
    }
    for path, expected in dataset.items():
        got = get_file_for_path(path)
        assert got == expected, \
            f"path {path} normalized to {got},\
                 while {expected} expected"

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
