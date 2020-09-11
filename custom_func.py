import os

from Consts import project_dir
from errors import NotFound


def build_path(path: str) -> str:
    resultpath = path
    if not path:
        resultpath = "/"
    elif resultpath[-1] != "/":
        resultpath = f"{resultpath}/"

    return resultpath

def get_contenttype(file_path: str) -> str:
    if not file_path:
        return "html"
    try:
        file_type = file_path.split(".")[1].lower()
        content_type_by_extension = {
            "gif": "gif",
            "jpeg": "jpeg",
            "jpg": "jpeg",
            "png": "png",
            "svg": "svg+xml",
            "css": "css",
            "html": "html"
        }
        content_type = content_type_by_extension[file_type]
    except IndexError:
        content_type = None
    return content_type

def to_bytes(massage: str) -> bytes:
    if isinstance(massage, str):
        massage = massage.encode()
    return massage
    return massage


def save_user_qs_to_file(query: str):
    qs_file = project_dir / "storage" / "xxx.txt"

    with qs_file.open("w") as dst:
        dst.write(query)


def get_user_qs_from_file():
    qs_file = project_dir / "storage" / "xxx.txt"
    if not qs_file.is_file():
        return ""

    with qs_file.open("r") as src:
        content = src.read()

    if isinstance(content, bytes):
        content = content.decode()

    return content

def delete_file():
    qs_file = project_dir / "storage" / "xxx.txt"
    if not qs_file.is_file():
        return ""

    os.remove(qs_file)

def get_qs_fromPostRequest(headers, rfile) -> str:
    content_length_str = headers.get("content-length", 0)
    content_length = int(content_length_str)

    if not content_length:
        return""

    payload_bytes = rfile.read(content_length)
    payload = payload_bytes.decode()
    return payload


def name_validation(names: str):
    if not names.isalnum() or names.isdigit():
        raise ValueError("MUST contain letters")

    lmin, lmax = 0, 20
    if not lmin <= len(names) <= lmax:
        raise ValueError(f"MUST have length between {lmin}..{lmax} chars")


def validate_age(age: str) -> None:
    if isinstance(age, str) and not age.isdecimal():
        raise ValueError("MUST contain digits only")

    value = int(age)
    if value <= 0:
        raise ValueError("MUST be positive integer")

def read_content(path: str):
    static_obj = project_dir / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content
