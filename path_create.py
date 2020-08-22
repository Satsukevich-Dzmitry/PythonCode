def build_path(path : str) -> str:
    resultpath = path
    if not path:
        resultpath = "/"
    elif resultpath[-1] != "/":
        resultpath = f"{resultpath}/"
    return resultpath

def get_file_for_path(url) -> tuple:
    path = build_path(url)
    splited_path = path.split("/")

    try:
        file_path = splited_path[-2]
    except IndexError:
        file_path = None
    path = build_path(splited_path[1])
    path = f"/{path}" if path != "/" else path

    return path, file_path

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
            }
        content_type = content_type_by_extension[file_type]
    except IndexError:
        content_type = None

    return content_type
