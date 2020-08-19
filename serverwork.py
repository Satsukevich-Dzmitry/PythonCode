
from pathlib import Path
from http.server import SimpleHTTPRequestHandler
import Consts
import Path_create
import to_bytes

project_dir = Path(__file__).parent.resolve()  #Для привязки к файлу,затем переход к папке(родитель)и выдача его пути

class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
        #return SimpleHTTPRequestHandler.do_GET(self)
        return super().do_GET()#унаследовался от родительского класса

    def handle_hello(self):
        content = f"""
                <html>
                <head>
                <title>XXX</title>
                <link rel="stylesheet" href="/Style/hello.css/"
                </head>
                <body>
                <h1>hello world</h1>
                <p>{self.path}</p>
                </body>
                </html>
                """

        self.respond(message=content)

    def handle_congrats(self):
        content = self.import_file("congrats.html", "r", "text", "html")
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

    def respond(self, message, code=200, content_type="text/html", max_age=Consts.CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        message = to_bytes.to_bytes(message)
        self.wfile.write(message)



    def import_file(self, path, mode="rb", content="image", filetype="jpg"):
        file = project_dir/path
        if not file.exists():
            return self.handle_404()
        with file.open(mode) as fp:
            file = fp.read()
        self.respond(file, content_type=f"{content}/{filetype}")


    def do_GET(self):
        path = Path_create.build_path(self.path)
        if path == "/":
            self.handle_root()
        elif path == "/unnamed.png/":
            self.import_file("unnamed.png", "rb", "image", "png")
        elif path == "/IMG_1335.jpg/":
            self.import_file("IMG_1335.jpg", "rb", "image" "jpg")
        elif path == "/hello/":
            self.handle_hello()
        elif path == "/Style/hello.css/":
            self.import_file("./Style/hello.css", "r", "text", "css")
        elif path == "/congrats/":
            self.handle_congrats()
        elif path == "/Happy_winner.png/":
            self.import_file("Happy_winner.png", "rb", "image" "png")
        else:
            self.handle_404()