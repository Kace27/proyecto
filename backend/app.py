from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import sqlite3
import os
import logging
import sys

# Configurar logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurar CORS correctamente
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:8000",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"]
    }
})

# Ruta de prueba específica para probar CORS
@app.route('/test-cors', methods=['GET', 'OPTIONS'])
def test_cors():
    logger.info("Recibida solicitud a /test-cors")
    response = jsonify({"message": "CORS funcionando"})
    return response

@app.after_request
def after_request(response):
    # Imprimir información sobre la solicitud para depuración
    logger.debug(f"Procesando solicitud: {request.method} {request.path}")
    logger.debug(f"Cabeceras de solicitud: {dict(request.headers)}")
    logger.debug(f"Cabeceras de respuesta: {dict(response.headers)}")
    return response

# Database setup
DATABASE_PATH = 'employees.db'

def init_db():
    """Initialize the database and create tables if they don't exist"""
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        )
        ''')
        
        # Insert some sample data
        sample_data = [
            ('1234', 'Juan Pérez'),
            ('5678', 'Ana García'),
            ('9012', 'Carlos Rodríguez'),
            ('4321', 'María López'),
            ('8765', 'Pedro Sánchez')
        ]
        
        cursor.executemany('INSERT INTO employees (pin, name) VALUES (?, ?)', sample_data)
        conn.commit()
        conn.close()
        logger.info("Database initialized with sample data.")

@app.route('/verify_pin', methods=['POST'])
def verify_pin():
    """Verify PIN and return employee information if valid"""
    logger.info("Recibida solicitud POST a /verify_pin")
    
    # Imprimir cuerpo de la solicitud
    logger.debug(f"Cuerpo de la solicitud: {request.get_data(as_text=True)}")
    
    data = request.json
    if not data:
        logger.error("No se pudo parsear JSON del cuerpo de la solicitud")
        return jsonify({'success': False, 'message': 'Formato de solicitud inválido.'}), 400
    
    pin = data.get('pin')
    logger.info(f"PIN recibido: {pin}")
    
    if not pin or len(pin) != 4 or not pin.isdigit():
        return jsonify({'success': False, 'message': 'PIN inválido. Debe ser de 4 dígitos.'}), 400
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT name FROM employees WHERE pin = ?', (pin,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        logger.info(f"PIN válido, empleado encontrado: {result[0]}")
        return jsonify({
            'success': True,
            'employee': {
                'name': result[0]
            }
        })
    else:
        logger.info("PIN no encontrado en la base de datos")
        return jsonify({'success': False, 'message': 'PIN no encontrado.'}), 404

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    init_db()  # Initialize database on startup
    app.run(debug=True, host='0.0.0.0', port=5002) 