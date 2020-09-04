from http.server import SimpleHTTPRequestHandler
import Consts
import custom_func
from Consts import project_dir
from custom_func import save_user_qs_to_file, get_user_qs_from_file, get_qs_fromPostRequest
from errors import NotFound
import traceback
from errors import MethodNotAllowed
from custom_class import RequestHttp
from web_app_namespace import Web_App_Names


class MyHandler(SimpleHTTPRequestHandler):
    def respond(self, message, code=200, content_type="text/html", max_age=Consts.CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        message = custom_func.to_bytes(message)
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        self.wfile.write(message)

    def redirect(self, to: str):
        self.send_response(302)
        self.send_header("Location", to)
        self.end_headers()

    def handle_hello(self, endpoint: RequestHttp):
        if endpoint.method != "get":
            raise MethodNotAllowed

        query_string = get_user_qs_from_file()
        name_dict = Web_App_Names.get_qs_info(query_string)
        content = f"""
                <html>
                <head>
                <title>Hello Page</title>
                <link rel="stylesheet" href="/style/hello.css/">
                </head>
                <body>
                <h1 class="ribbon"><strong class="ribbon-content">Hello {name_dict.name} {name_dict.surname}!</strong></h1>
                <h1>{name_dict.year}!</h1>
                 <form action="/handle_hello_update/" method="post">
                    <label for="xxx-id">Your name:</label>
                    <input type="text" name="name" id="xxx-id">
                    <label for="surname-id" >Your surname:</label>
                    <input type="text" name="surname" id="surname-id">
                    <label for="age-id">Your age:</label>
                    <input type="text" name="age" id="age-id">
                    <button type="submit">Thanks</button>
                </form>
                <p><a href="/html_files/index.html" class="btn"> Opening_page </a></p>
                </body>
                </html>
                """

        self.respond(content)

    def import_file(self, path, mode="rb", content="image", filetype="jpg"):
        file = project_dir / path
        if not file.exists():
            return self.import_file("html_files/404.html", "r", "text", "html")
        with file.open(mode) as fp:
            file = fp.read()
        self.respond(file, content_type=f"{content}/{filetype}")

    def do_GET(self):
        return self.do_request("get")

    def do_POST(self):
        return self.do_request("post")

    def handle_hello_update(self, request: RequestHttp):
        if request.method != "post":
            raise MethodNotAllowed

        qs = get_qs_fromPostRequest(self.headers, self.rfile)
        save_user_qs_to_file(qs)
        self.redirect("/hello")

    def do_request(self, http_method):
        request = RequestHttp.from_path(self.path, method=http_method)
        requests = {
                    "/hello/": [self.handle_hello, [request]],
                    "/style/": [self.import_file, [f"styles/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/images/": [self.import_file, [f"images/{request.file_name}", "rb", "image", f"{request.contenttype}"]],
                    "/html_files/": [self.import_file, [f"html_files/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/handle_hello_update/": [self.handle_hello_update, [request]],
                    }
        try:
            handler, args = requests[request.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.import_file("html_files/404.html", "r", "text", "html")
        except MethodNotAllowed:
            self.respond("", code=405, content_type="text/plain")
        except Exception:
            self.respond(traceback.format_exc(), code=500, content_type="text/plain")


