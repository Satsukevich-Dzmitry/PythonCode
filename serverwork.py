import os
from http.server import SimpleHTTPRequestHandler
import Consts
import custom_func
from Consts import project_dir
from Errors_func import Html_colors
from custom_func import save_user_qs_to_file, get_user_qs_from_file, get_qs_fromPostRequest
from errors import NotFound
import traceback
from errors import MethodNotAllowed
from custom_class import Request_http
from User_data import User_name


class MyHandler(SimpleHTTPRequestHandler):
    def respond(self, message, code=200, content_type="text/html", max_age=Consts.CACHE_AGE, set_cookies=""):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        message = custom_func.to_bytes(message)
        self.send_header("Content-Length", str(len(message)))
        if set_cookies:
            self.send_header("Set-Cookie", f"{set_cookies}")
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        self.wfile.write(message)

    def redirect(self, to: str, set_cookies=""):
        self.send_response(302)
        self.send_header("Location", to)
        if set_cookies:
            self.send_header("Set-Cookie", f"{set_cookies}")
        self.end_headers()

    def render_hello(self, Names: str):
        name_dict = User_name.get_qs_info(Names)
        file = custom_func.read_content("html_files/hello.html").decode()
        text_color = Html_colors.html_colors(name_dict)
        session_ID= custom_func.get_session(self.headers)
        theme = custom_func.get_theme_from_file(session_ID)
        page_data = {
            "user_name": name_dict.name,
            "user_surname": name_dict.surname,
            "user_year": name_dict.year,
            "user_age": name_dict.age,
            "html_text_color": text_color.text_color,
            "html_input_color": text_color.input_color,
            "theme": theme,
        }
        content = file.format(**page_data)
        return content

    def handle_hello(self, endpoint: Request_http):
        if endpoint.method != "get":
            raise MethodNotAllowed
        sessionID = self.headers.get("Cookie")
        if not sessionID:
            sessionID = str(self.generate_session())
            query_string = get_user_qs_from_file(sessionID)
            content = self.render_hello(query_string)
            self.respond(content, set_cookies=sessionID)
        query_string = get_user_qs_from_file(sessionID)
        content = self.render_hello(query_string)
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

    @staticmethod
    def generate_session():
        return str(os.urandom(16).hex())


    def handle_hello_update(self, request: Request_http, User: User_name):
        if request.method != "post":
            raise MethodNotAllowed
        qs = get_qs_fromPostRequest(self.headers, self.rfile)
        sessionID = custom_func.get_session(self.headers)
        if not sessionID:
            sessionID = self.generate_session()
        user = User.get_qs_info(qs)
        check = user.valid
        if check:
            save_user_qs_to_file(qs, sessionID)
            self.redirect("/hello")

        else:
            content = self.render_hello(qs)
            self.respond(content)


    def reset_data(self, request: Request_http):
        if request.method != "post":
            raise MethodNotAllowed
        sessionID = custom_func.get_session(self.headers)
        qs_file = project_dir / "storage" / f"sessionID={sessionID}.json"
        if os.path.exists(qs_file):
            os.remove(qs_file)
        self.redirect("/hello", set_cookies=f"{sessionID}; Max-Age=-1; Path=/")


    def set_background(self, request: Request_http):
        if request.method != "post":
            raise MethodNotAllowed
        sessionID = custom_func.get_session(self.headers)
        current_theme = custom_func.get_theme_from_file(sessionID)
        new_theme = custom_func.switch_theme(current_theme)
        custom_func.save_theme_to_file(sessionID, new_theme)
        self.redirect("/hello")

    def do_request(self, http_method):
        request = Request_http.from_path(self.path, method=http_method)
        user = User_name
        requests = {
                    "/hello/": [self.handle_hello, [request]],
                    "/style/": [self.import_file, [f"styles/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/images/": [self.import_file, [f"images/{request.file_name}", "rb", "image", f"{request.contenttype}"]],
                    "/html_files/": [self.import_file, [f"html_files/{request.file_name}", "r", "text", f"{request.contenttype}"]],
                    "/handle_hello_update/": [self.handle_hello_update, [request, user]],
                    "/reset/": [self.reset_data, [request]],
                    "/set_background/": [self.set_background, [request]],
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


