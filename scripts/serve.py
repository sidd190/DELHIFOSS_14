#!/usr/bin/env python3
"""Serve the kit and pinned Precogly frontend on loopback; no dependencies."""
import functools
import http.server
import pathlib
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Precogly(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0].startswith('/guest'):
            self.path = '/index.html'
        super().do_GET()


def main():
    servers = []
    try:
        for port, directory, handler in [(4173, ROOT, http.server.SimpleHTTPRequestHandler),
                                         (4174, ROOT / 'vendor/precogly/app', Precogly)]:
            server = http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(handler, directory=str(directory)))
            servers.append(server)
            threading.Thread(target=server.serve_forever, daemon=True).start()
        print('Talk kit: http://127.0.0.1:4173\nPrecogly: http://127.0.0.1:4174/guest\nCtrl+C to stop.', flush=True)
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    main()
