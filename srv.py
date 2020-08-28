import socketserver

import Consts
import serverwork


if __name__ == "__main__":
    with socketserver.TCPServer(("", serverwork.Consts.PORT), serverwork.MyHandler) as httpd:
        print("works", Consts.project_dir)
        httpd.serve_forever(poll_interval=1)
