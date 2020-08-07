import socketserver
import serverwork


if __name__ == "__main__":
    with socketserver.TCPServer(("", serverwork.Consts.PORT), serverwork.MyHandler) as httpd:
        print("works", serverwork.project_dir)
        httpd.serve_forever(poll_interval=1)
