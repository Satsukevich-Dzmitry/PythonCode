from pathlib import Path
from http.server import SimpleHTTPRequestHandler
import Consts
import path_create
import to_bytes
from errors import NotFound
import traceback
from errors import MethodNotAllowed


project_dir = Path(__file__).parent.resolve()  # Для привязки к файлу,затем переход к папке(родитель)и выдача его пути


class MyHandler(SimpleHTTPRequestHandler):
    def respond(self, message, code=200, content_type="text/html", max_age=Consts.CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        message = to_bytes.to_bytes(message)
        self.wfile.write(message)

    def import_file(self, path, mode="rb", content="image", filetype="jpg"):
        file = project_dir / path
        if not file.exists():
            return self.import_file("html_files/404.html", "r", "text", "html")
        with file.open(mode) as fp:
            file = fp.read()
        self.respond(file, content_type=f"{content}/{filetype}")

    def do_GET(self):
        path, file_path = path_create.get_file_for_path(self.path)
        content_type = path_create.get_contenttype(file_path)
        requests = {
                    "/": [self.import_file, ["html_files/index.html", "r", "text", "html"]],
                    "/hello/": [self.import_file, ["html_files/hello.html", "r", "text", "html"]],
                    "/congrats/": [self.import_file, ["html_files/congrats.html", "r", "text", "html"]],
                    "/style/": [self.import_file, [f"styles/{file_path}", "r", "text", "css"]],
                    "/images/": [self.import_file, [f"images/{file_path}", "rb", "image", f"{content_type}"]],
                    "/html_files/": [self.import_file, [f"html_files/{file_path}", "r", "text", "html"]],
                    }
        try:
            handler, args = requests[path]
            handler(*args)
        except (NotFound, KeyError):
            self.import_file("html_files/404.html", "r", "text", "html")
        except MethodNotAllowed:
            self.respond("", code=405, content_type="text/plain")
        except Exception:
            self.respond(traceback.format_exc(), code=500, content_type="text/plain")
