import os
import socketserver
from http.server import SimpleHTTPRequestHandler
#from PIL import Image

PORT = int(os.getenv("PORT", 8000))

CACHE_AGE = 60 * 60 * 12



class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
       # img = Image.open("e:/python/PythonCode/unnamed.png", "r")
        #img.save("unnamed.png", "png")
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
        #img = Image.open("e:/python/PythonCode/IMG_1335.jpg", "r")
        #img.save("IMG_1335.jpg")
        #img.show()
        #img = Image.open(IMG_1335.jpg)
        msg = f"""
                <html>
                 <head>
                <meta charset="utf-8">
                <style>
                <body>
                 background-image: url("e://python/Pythoncode/IMG_1335.jpg") no-repeat;
                background-size:100%;
                  <body/>
                </style>
                </head>
                 <body>
                <p></p>
                 </body>
                </html>
                """
        self.respond(message=msg, code=404, content_type="text/html")

    def respond(self, message, code=200, content_type="text/html", max_age=CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age=<{CACHE_AGE}>")
        self.end_headers()
        self.wfile.write(message.encode())

    def build_path(self) -> str:
        result = self.path
        if result[-1] != "/":
            result = f"{result}/"
        return result

    def do_GET(self):

        path = self.build_path()

        if path == "/":
            self.handle_root()
        elif path == "/hello/":
            self.handle_hello()
        else:
            self.handle_404()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("works")
        httpd.serve_forever(poll_interval=1)
