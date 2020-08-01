import os
import socketserver
from http.server import SimpleHTTPRequestHandler

PORT = int(os.getenv("PORT", 8000))

CACHE_AGE = 60 * 60 * 24


class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
        return SimpleHTTPRequestHandler.do_GET(self)
        #return super().do_GET()#унаследовался от родительского класса

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
                <head><title>XXX</title></head>
                <body>
                <h1>SORRY NOT FOUND</h1>
                </body>
                </html>
                """
        self.respond(message=msg, code=404, content_type="text/html")

    def respond(self, message, code=200, content_type="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
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
        elif path == "hello":
            self.handle_hello()
        else:
            self.handle_404


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("works")
        httpd.serve_forever(poll_interval=1)
