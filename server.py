"""
Serves files out of its current directory.
Doesn't handle POST requests.
"""
import SocketServer
import SimpleHTTPServer
import os
from renderers.directory import DirectoryRenderer
import urllib

#CONSTANTS
PORT = 9191




#a list of renders. Will call can_render(path) and choose the first one that returns true
renderers = [DirectoryRenderer()]

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        decoded_path = urllib.unquote(self.path)
        print decoded_path

        #self.wfile.write(self.render_dir(self.path))  # call sample function here
        if self.path == '/favicon.ico':
            self.send_response(40)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        elif self.path.startswith('/~~/'):
             #serve assets
             self.path = os.getcwd() + '/assets/' + self.path[4:]
             SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        #see if we can render this!
        for r in renderers:
            if r.can_render(decoded_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(r.render(decoded_path))
                return

       #ok ... we didn't havea  renderer so just serve it up it and hope for the best
        print "file " + str(self.path)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def translate_path(self, path):
        return path


if __name__ == "__main__":
    SocketServer.TCPServer.allow_reuse_address = True
    httpd = SocketServer.ThreadingTCPServer(('localhost', PORT),CustomHandler)

    print "serving at port", PORT
    httpd.serve_forever()