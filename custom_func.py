import json
import os
from typing import Optional

from Consts import project_dir, DEFAULT_THEME, THEMES
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


def save_user_qs_to_file(profile: str, sessionID: str):
    qs_file = project_dir / "storage" / f"sessionID={sessionID}.json"
    data = {
        "profile": profile,
    }
    with qs_file.open("w") as dst:
        json.dump(data, dst)

#Изменить
def switch_theme(current_theme: Optional[str]) -> str:
    themes = sorted(THEMES)
    themes_fsm = {th1: th2 for th1, th2 in zip(themes, reversed(themes))}

    new_theme = themes_fsm[current_theme or DEFAULT_THEME]

    return new_theme

def save_theme_to_file(sessionID: str, new_theme: str):
    session_data = get_file(sessionID)
    session_data.update({"theme": new_theme} or {})

    data_file = project_dir / "storage" / f"sessionID={sessionID}.json"
    with data_file.open("w") as dst:
        json.dump(session_data, dst)

def get_file(sessionID: str):
    qs_file = project_dir / "storage" / f"sessionID={sessionID}.json"
    empty_dict = {}
    if not qs_file.is_file():
        return empty_dict

    with qs_file.open("r") as src:
        data = json.load(src)

    return data or empty_dict

def get_theme_from_file(sessionID: str):
    qs_file = project_dir / "storage" / f"sessionID={sessionID}.json"
    if not qs_file.is_file():
        return None

    with qs_file.open("r") as src:
        content = json.load(src)

    return content.get("theme", DEFAULT_THEME)

def get_user_qs_from_file(sessionID: str):
    qs_file = project_dir / "storage" / f"sessionID={sessionID}.json"
    if not qs_file.is_file():
        return None

    with qs_file.open("r") as src:
        content = json.load(src)

    return content.get("profile")

def get_qs_fromPostRequest(headers, rfile) -> str:
    content_length_str = headers.get("content-length", 0)
    content_length = int(content_length_str)

    if not content_length:
        return""

    payload_bytes = rfile.read(content_length)
    payload = payload_bytes.decode()
    return payload

def get_session(headers):
    session_number = headers.get("Cookie", 0)

    if not session_number:
        return ""

    return session_number


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
