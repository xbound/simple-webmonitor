from http.server import BaseHTTPRequestHandler, HTTPServer

from jinja2 import Environment, BaseLoader

from parser import CACHE



class SinglePageRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        with open('./templates/index.html','r') as html_file:
            page = html_file.read()

        content = Environment(loader=BaseLoader).from_string(page).render({'cache':CACHE})

        self.wfile.write(content.encode('utf-8'))


def runserver(port):
    httpd = HTTPServer(('',port),SinglePageRequestHandler)
    try:
        print("Starting HTTP server: http://127.0.0.1:{}...".format(port))
        httpd.serve_forever()
    finally:
        print("Closing HTTP server on port {}...".format(port))
        httpd.server_close()
if __name__ == '__main__':
    runserver(9000)
