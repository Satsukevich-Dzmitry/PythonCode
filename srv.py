import os
import socketserver
from pathlib import Path
from http.server import SimpleHTTPRequestHandler
import Try
#from PIL import Image

project_dir = Path(__file__).parent.resolve()#Для привязки к нынешнему файлу, затем переход к папке(родитель) и выдача его пути

class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
        #return SimpleHTTPRequestHandler.do_GET(self)
        return super().do_GET()#унаследовался от родительского класса

    def handle_hello(self):
        content = f"""
                <html>
                <head><title>XXX</title></head>
                <body>
                <h1>hello world</h1>
                <p>{self.path}</p>
                </body>
                </html>
                """

        self.respond(message=content)

    def handle_404(self):
        msg = f"""
                <html>
                 <head>
                <meta charset="utf-8">
                <style type="text/css">
                body {{ 
                    background: url("/IMG_1335.jpg/") no-repeat;
                    background-size:100%;
                }}
                </style>
                </head>
                 <body>
                <p>check</p>
                 </body>
                </html>
                """
        self.respond(message=msg, code=404, content_type="text/html")

    def respond(self, message, code=200, content_type="text/html", max_age=Try.CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        if isinstance(message,str):
            message = message.encode()
        self.wfile.write(message)

    def build_path(self) -> str:
        result = self.path
        if result[-1] != "/":
            result = f"{result}/"
        return result


    def import_file(self, path, mode="rb", content="image", filetype="jpg"):
        img = project_dir/path
        if not img.exists():
            return self.handle_404()
        with img.open(mode) as fp:
            img = fp.read()
        self.respond(img, content_type=f"{content}/{filetype}")


    def do_GET(self):
        path = self.build_path()
        if path == "/":
            self.handle_root()
        elif path == "/unnamed.png/":
            self.import_file("unnamed.png", "rb", "image", "png")
        elif path == "/IMG_1335.jpg/":
            self.import_file("IMG_1335.jpg", "rb", "image" "jpg")
        elif path == "/hello/":
            self.handle_hello()
        else:
            self.handle_404()


if __name__ == "__main__":
    with socketserver.TCPServer(("", Try.PORT), MyHandler) as httpd:
        print("works", project_dir)
        httpd.serve_forever(poll_interval=1)
