from path_create import build_path
from to_bytes import to_bytes


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
            f"{original} didnt correctly turned into bytes"
