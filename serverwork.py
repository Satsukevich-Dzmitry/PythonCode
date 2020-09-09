from http.server import SimpleHTTPRequestHandler
import Consts
import custom_func
from Consts import project_dir
from custom_func import save_user_qs_to_file, get_user_qs_from_file, get_qs_fromPostRequest
from errors import NotFound
import traceback
from errors import MethodNotAllowed
from custom_class import Request_http
from User_data import User_name


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

    def render_hello(self, Names: str):
        name_dict = User_name.get_qs_info(Names)
        file = custom_func.read_content("html_files/hello.html").decode()
        page_data = {
            "user_name": name_dict.name,
            "user_surname": name_dict.surname,
            "user_year": name_dict.year,
        }
        content = file.format(**page_data)
        self.respond(content)

    def handle_hello(self, endpoint: Request_http):
        if endpoint.method != "get":
            raise MethodNotAllowed

        query_string = get_user_qs_from_file()
        self.render_hello(query_string)

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

    def handle_hello_update(self, request: Request_http, User: User_name):
        if request.method != "post":
            raise MethodNotAllowed
        qs = get_qs_fromPostRequest(self.headers, self.rfile)
        user = User.get_qs_info(qs)
        check = user.valid
        if check:
            save_user_qs_to_file(qs)
            self.redirect("/hello")
        else:
            self.render_hello(qs)



    def do_request(self, http_method):
        request = Request_http.from_path(self.path, method=http_method)
        user = User_name
        requests = {
                    "/hello/": [self.handle_hello, [request]],
                    "/style/": [self.import_file, [f"styles/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/images/": [self.import_file, [f"images/{request.file_name}", "rb", "image", f"{request.contenttype}"]],
                    "/html_files/": [self.import_file, [f"html_files/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/handle_hello_update/": [self.handle_hello_update, [request, user]],
                    }
        try:
            try:
                handler, args = requests[request.normal]
            except KeyError:
                raise NotFound

            handler(*args)
        except NotFound:
            self.import_file("html_files/404.html", "r", "text", "html")
        except MethodNotAllowed:
            self.respond("", code=405, content_type="text/plain")
        except Exception:
            self.respond(traceback.format_exc(), code=500, content_type="text/plain")


