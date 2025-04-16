import http.server
import socketserver
import os

# Configuración
PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

print(f"Servidor de pantalla de cocina iniciado en el puerto {PORT}")
print(f"Abre un navegador y visita: http://localhost:{PORT}/kitchen.html")
print("Presiona Ctrl+C para detener el servidor")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close() 