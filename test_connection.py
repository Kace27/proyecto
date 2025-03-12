#!/usr/bin/env python
"""
Test de conexión entre frontend y backend para la aplicación de Verificación de PIN.
Este script inicia el servidor Flask y el servidor frontend, verifica que el endpoint
esté disponible y responda correctamente, y abre el navegador automáticamente.
"""
import os
import sys
import time
import json
import threading
import webbrowser
import requests
import argparse
import sqlite3
from urllib.parse import urljoin

# Procesar argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Test de conexión frontend-backend para Verificación de PIN')
parser.add_argument('--port', type=int, default=5000, help='Puerto para el servidor backend (por defecto: 5000)')
parser.add_argument('--frontend-port', type=int, default=8000, help='Puerto para el servidor frontend (por defecto: 8000)')
args = parser.parse_args()

# Configuración
HOST = '127.0.0.1'
PORT = args.port
FRONTEND_PORT = args.frontend_port
BASE_URL = f'http://{HOST}:{PORT}'

# Endpoints para probar
ENDPOINTS = [
    {'url': '/verify_pin', 'method': 'POST', 'name': 'Verificar PIN', 'data': {'pin': '1234'}}
]

def verify_database():
    """Verifica que la base de datos exista o la crea con datos de ejemplo"""
    print("\n🔍 Verificando base de datos...")
    db_path = os.path.join('backend', 'employees.db')
    
    # Si la base de datos no existe, crearla
    if not os.path.exists(db_path):
        print("⚠️  Base de datos no encontrada, creando una nueva...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla de empleados
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        )
        ''')
        
        # Insertar datos de ejemplo
        sample_data = [
            ('1234', 'Juan Pérez'),
            ('5678', 'Ana García'),
            ('9012', 'Carlos Rodríguez'),
            ('4321', 'María López'),
            ('8765', 'Pedro Sánchez')
        ]
        
        try:
            cursor.executemany('INSERT INTO employees (pin, name) VALUES (?, ?)', sample_data)
            conn.commit()
            print("✅ Base de datos creada e inicializada correctamente.")
        except sqlite3.IntegrityError:
            print("⚠️  La base de datos ya contiene algunos registros.")
            conn.rollback()
        finally:
            conn.close()
    else:
        print("✅ Base de datos encontrada.")

def run_flask_server():
    """Ejecuta el servidor Flask en un hilo separado"""
    import subprocess
    
    try:
        # Cambiar al directorio backend
        os.chdir('backend')
        
        # Ejecutar app.py como un proceso independiente
        process = subprocess.Popen([sys.executable, 'app.py'])
        
        # Volver al directorio original
        os.chdir('..')
        
        # Esperar hasta que termine (no debería terminar a menos que haya error)
        return process
    except Exception as e:
        print(f"\n❌ ERROR al iniciar el servidor Flask: {str(e)}")
        sys.exit(1)

def run_frontend_server():
    """Ejecuta el servidor frontend en un hilo separado"""
    import subprocess
    
    try:
        # Cambiar al directorio frontend
        os.chdir('frontend')
        
        # Ejecutar server.py como un proceso independiente
        process = subprocess.Popen([sys.executable, 'server.py'])
        
        # Volver al directorio original
        os.chdir('..')
        
        # Esperar hasta que termine (no debería terminar a menos que haya error)
        return process
    except Exception as e:
        print(f"\n❌ ERROR al iniciar el servidor frontend: {str(e)}")
        sys.exit(1)

def test_endpoints():
    """Prueba los endpoints del backend"""
    print("\n🔍 Probando endpoints del backend...")
    print("=" * 50)
    
    all_successful = True
    
    for endpoint in ENDPOINTS:
        url = f"{BASE_URL}{endpoint['url']}"
        method = endpoint['method']
        name = endpoint['name']
        data = endpoint.get('data', {})
        
        try:
            # Esperar a que el servidor esté disponible
            time.sleep(3)
            
            # Realizar la petición
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            
            # Verificar respuesta
            if response.status_code in [200, 201, 404]:  # 404 es aceptable en caso de PIN inválido
                # Intentar parsear respuesta JSON
                try:
                    data = response.json()
                    print(f"✅ {name}: OK (Status: {response.status_code})")
                    if 'success' in data:
                        print(f"   Respuesta: {data}")
                except json.JSONDecodeError:
                    print(f"❌ {name}: Error al parsear respuesta JSON (Status: {response.status_code})")
                    all_successful = False
            else:
                print(f"❌ {name}: Error (Status: {response.status_code})")
                all_successful = False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Error de conexión. Asegúrate de que el servidor esté corriendo.")
            all_successful = False
        except Exception as e:
            print(f"❌ {name}: Error inesperado: {str(e)}")
            all_successful = False
    
    print("=" * 50)
    
    return all_successful

def open_browser():
    """Abre el navegador con la interfaz frontend"""
    print("\n🌐 Abriendo interfaz en el navegador...")
    time.sleep(2)  # Esperar un poco para que los servidores estén listos
    webbrowser.open(f'http://localhost:{FRONTEND_PORT}/index.html')
    print(f"Accede directamente a: http://localhost:{FRONTEND_PORT}/index.html si el navegador muestra un listado de directorio")

def main():
    """Función principal que ejecuta las pruebas de conexión"""
    print("\n" + "=" * 50)
    print("    PRUEBA DE CONEXIÓN SISTEMA DE VERIFICACIÓN DE PIN")
    print("=" * 50)
    print(f"Backend puerto: {PORT}, Frontend puerto: {FRONTEND_PORT}")
    
    # Verificar que existan las carpetas necesarias
    if not os.path.exists('backend'):
        print("❌ Error: No se encontró la carpeta 'backend'.")
        return
    
    if not os.path.exists('frontend'):
        print("❌ Error: No se encontró la carpeta 'frontend'.")
        return
    
    # Verificar la base de datos
    verify_database()
    
    # Iniciar el servidor Flask como un proceso independiente
    print("\n🚀 Iniciando servidor Flask...")
    flask_process = run_flask_server()
    
    # Iniciar el servidor frontend como un proceso independiente
    print("\n🚀 Iniciando servidor frontend...")
    frontend_process = run_frontend_server()
    
    try:
        # Probar endpoints del backend
        endpoints_ok = test_endpoints()
        
        if endpoints_ok:
            # Abrir el navegador
            open_browser()
        
        print("\n📝 Instrucciones de uso:")
        print("1. El frontend se ha abierto en tu navegador.")
        print(f"2. El backend está ejecutándose en http://{HOST}:{PORT}")
        print("3. Presiona Enter en la terminal para detener los servidores.")
        print("\nPara usar puertos diferentes:")
        print(f"  python {sys.argv[0]} --port <puerto_backend> --frontend-port <puerto_frontend>")
        
        # Esperar a que el usuario presione Enter para salir
        input("\n⏳ Presiona Enter para detener los servidores...\n")
            
    except KeyboardInterrupt:
        print("\n👋 Deteniendo servidores...")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
    finally:
        # Terminar los procesos
        if 'flask_process' in locals():
            flask_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        print("\n✨ Prueba de conexión finalizada.")

if __name__ == "__main__":
    main() 