from itertools import takewhile
from typing import NamedTuple
from typing import Optional

from custom_func import get_contenttype


class Request_http(NamedTuple):
    method: str
    original: str
    normal: str
    contenttype: str
    file_name: Optional[str]
    query_string: Optional[str]

    @classmethod
    def from_path(cls, path: str, method: str) -> "Request_http":
        if not path:
            return Request_http(method="get", original="", normal="/", contenttype="html", file_name=None, query_string=None)

        xxx = path.split("?")
        if len(xxx) == 2:
            path, qs = xxx
        else:
            path, qs = xxx[0], None

        parts = tuple(filter(bool, path.split("/")))
        compiled = "/".join(takewhile(lambda part: "." not in part, parts))
        if compiled not in ("", "/"):
            normal = f"/{compiled}/"
            last = parts[-1] if parts else ""
            file_name = last if "." in last else None
        else:
            normal = "/html_files/"
            file_name = "index.html"
        contenttype = get_contenttype(file_name)
        return Request_http(
            method=method, original=path, normal=normal, contenttype=contenttype, file_name=file_name, query_string=qs
        )