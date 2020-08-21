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
    def handle_root(self):
        return super().do_GET()  # унаследовался от родительского класса

    def handle_404(self):
        self.import_file("html_files/404.html", "r", "text", "html")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

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
            return self.handle_404()
        with file.open(mode) as fp:
            file = fp.read()
        self.respond(file, content_type=f"{content}/{filetype}")

    def do_GET(self):
        path = path_create.build_path(self.path)

        handlers = {
                    "/": [self.handle_root, []],
                    "/hello/": [self.import_file, ["html_files/hello.html", "r", "text", "html"]],
                    "/congrats/": [self.import_file, ["html_files/congrats.html", "r", "text", "html"]],
                    "/hello.css/": [self.import_file, ["styles/hello.css", "r", "text", "css"]],
                    "/Happy_winner.png/": [self.import_file, ["images/Happy_winner.png", "rb", "image", "png"]],
                    "/unnamed.png/": [self.import_file, ["images/unnamed.png", "rb", "image", "png"]],
                    "/IMG_1335.jpg/": [self.import_file, ["images/IMG_1335.jpg", "rb", "image", "jpg"]],
                    }
        try:
            handler, args = handlers[path]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()
