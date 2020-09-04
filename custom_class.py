from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from urllib.parse import urlsplit

from custom_func import get_contenttype


class RequestHttp(NamedTuple):
    original: str
    normal: str
    contenttype: str
    method: str
    file_name: Optional[str]
    query_string: Optional[str]

    @classmethod
    def from_path(cls, path: str, method: str) -> "RequestHttp":
        if not path:
            return RequestHttp(method="get", original="", normal="/", contenttype="html", file_name=None, query_string=None)

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = (takewhile(lambda part: "." not in part, segments))
        compiled = "/".join(non_file_segments)
        if compiled not in ("", "/"):
            normal = f"/{compiled}/"
            last = segments[-1] if segments else ""
            file_name = last if "." in last else None
        else:
            normal = "/html_files/"
            file_name = "index.html"
        contenttype = get_contenttype(file_name)
        return RequestHttp(
            method=method or "get", original=path, normal=normal, contenttype=contenttype, file_name=file_name, query_string=components.query or None
        )