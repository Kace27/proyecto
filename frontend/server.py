import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Si la ruta solicitada es la raíz, redirige a index.html
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Garantizar que el directorio de trabajo sea el correcto
print(f"Directorio de trabajo: {os.getcwd()}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor frontend en http://localhost:{PORT}")
    print("Usa Ctrl+C para detener el servidor")
    httpd.serve_forever() 