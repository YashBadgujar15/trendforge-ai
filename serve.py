import http.server, socketserver, sys
PORT = 5501
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Serving on http://127.0.0.1:{PORT}", flush=True)
    httpd.serve_forever()
