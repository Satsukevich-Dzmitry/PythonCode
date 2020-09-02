def build_path(path: str) -> str:
    resultpath = path
    if not path:
        resultpath = "/"
    elif resultpath[-1] != "/":
        resultpath = f"{resultpath}/"
    return resultpath

def get_contenttype(file_path: str) ->str:
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