from Path_create import build_path


def test_normalize_path():
    dataset = {
        "/":"/",
        "/hello":"hello/",
        "hello///":"hello///",
        "/hello":"/hello/",
    }

    for path, expected in dataset.items():
        got = build_path(path)
        assert got == expected, f"path {path} normalized to {got}, while {expected} expected"