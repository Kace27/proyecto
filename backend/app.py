from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
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
DATABASE_PATH = 'employees.json'
TICKETS_PATH = 'tickets.json'
MENU_PATH = 'menu.json'

def load_employees():
    """Carga los empleados desde el archivo JSON"""
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Error al decodificar el archivo JSON")
            return {"employees": []}
    else:
        return {"employees": []}

def save_employees(data):
    """Guarda los empleados en el archivo JSON"""
    with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_tickets():
    """Carga los tickets desde el archivo JSON"""
    if os.path.exists(TICKETS_PATH):
        try:
            with open(TICKETS_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Error al decodificar el archivo de tickets JSON")
            return {"tickets": {}}
    else:
        return {"tickets": {}}

def save_tickets(data):
    """Guarda los tickets en el archivo JSON"""
    with open(TICKETS_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_menu():
    """Carga el menú desde el archivo JSON"""
    if os.path.exists(MENU_PATH):
        try:
            with open(MENU_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Error al decodificar el archivo de menú JSON")
            return {"categories": []}
    else:
        return {"categories": []}

def save_menu(data):
    """Guarda el menú en el archivo JSON"""
    with open(MENU_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def init_db():
    """Initialize the database if it doesn't exist"""
    # Inicializar empleados
    if not os.path.exists(DATABASE_PATH):
        # Datos de ejemplo
        data = {
            "employees": [
                {"id": 1, "pin": "1234", "name": "Juan Pérez", "role": "Mesero"},
                {"id": 2, "pin": "5678", "name": "Ana García", "role": "Gerente"},
                {"id": 3, "pin": "9012", "name": "Carlos Rodríguez", "role": "Mesero"},
                {"id": 4, "pin": "4321", "name": "María López", "role": "Administrador"},
                {"id": 5, "pin": "8765", "name": "Pedro Sánchez", "role": "Cocina"}
            ]
        }
        save_employees(data)
        logger.info("Base de datos JSON inicializada con datos de ejemplo.")
    
    # Inicializar menú si no existe
    if not os.path.exists(MENU_PATH):
        menu_data = {
            "categories": [
                {
                    "id": 1,
                    "name": "Categoria 1",
                    "items": [
                        {"id": 1, "name": "Articulo 1", "price": 100, "image": "https://placehold.co/122x84"},
                        {"id": 2, "name": "Articulo 2", "price": 120, "image": "https://placehold.co/122x84"},
                        {"id": 3, "name": "Articulo 3", "price": 90, "image": "https://placehold.co/122x84"},
                        {"id": 4, "name": "Articulo 4", "price": 150, "image": "https://placehold.co/122x84"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Categoria 2",
                    "items": [
                        {"id": 5, "name": "Articulo 5", "price": 80, "image": "https://placehold.co/122x84"},
                        {"id": 6, "name": "Articulo 6", "price": 110, "image": "https://placehold.co/122x84"},
                        {"id": 7, "name": "Articulo 7", "price": 130, "image": "https://placehold.co/122x84"},
                        {"id": 8, "name": "Articulo 8", "price": 95, "image": "https://placehold.co/122x84"}
                    ]
                }
            ]
        }
        save_menu(menu_data)
        logger.info("Menú JSON inicializado con datos de ejemplo.")
    
    # Inicializar tickets si no existe
    if not os.path.exists(TICKETS_PATH):
        tickets_data = {"tickets": {}}
        save_tickets(tickets_data)
        logger.info("Tickets JSON inicializado.")

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
    
    # Cargar empleados desde el archivo JSON
    db_data = load_employees()
    
    # Buscar el empleado con el PIN correspondiente
    employee = next((emp for emp in db_data["employees"] if emp["pin"] == pin), None)
    
    if employee:
        logger.info(f"PIN válido, empleado encontrado: {employee['name']}, rol: {employee['role']}")
        return jsonify({
            'success': True,
            'employee': {
                'name': employee['name'],
                'role': employee['role']
            }
        })
    else:
        logger.info("PIN no encontrado en la base de datos")
        return jsonify({'success': False, 'message': 'PIN no encontrado.'}), 404

@app.route('/employees', methods=['GET'])
def get_employees():
    """Retorna la lista de todos los empleados"""
    db_data = load_employees()
    return jsonify(db_data)

@app.route('/employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Actualiza la información de un empleado"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Datos inválidos'}), 400
    
    db_data = load_employees()
    
    # Buscar el empleado con el ID correspondiente
    employee_index = next((i for i, emp in enumerate(db_data["employees"]) if emp["id"] == employee_id), None)
    
    if employee_index is not None:
        # Actualizar los campos proporcionados
        for key, value in data.items():
            if key in db_data["employees"][employee_index] and key != "id":
                db_data["employees"][employee_index][key] = value
        
        save_employees(db_data)
        return jsonify({'success': True, 'employee': db_data["employees"][employee_index]})
    else:
        return jsonify({'success': False, 'message': 'Empleado no encontrado'}), 404

@app.route('/employee', methods=['POST'])
def add_employee():
    """Agrega un nuevo empleado"""
    data = request.json
    if not data or not all(key in data for key in ["pin", "name", "role"]):
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    
    db_data = load_employees()
    
    # Verificar que el PIN no esté en uso
    if any(emp["pin"] == data["pin"] for emp in db_data["employees"]):
        return jsonify({'success': False, 'message': 'El PIN ya está en uso'}), 400
    
    # Asignar un nuevo ID (el máximo actual + 1)
    new_id = max([emp["id"] for emp in db_data["employees"]], default=0) + 1
    
    # Crear el nuevo empleado
    new_employee = {
        "id": new_id,
        "pin": data["pin"],
        "name": data["name"],
        "role": data["role"]
    }
    
    # Agregar a la lista de empleados
    db_data["employees"].append(new_employee)
    save_employees(db_data)
    
    return jsonify({'success': True, 'employee': new_employee}), 201

@app.route('/menu', methods=['GET'])
def get_menu():
    """Retorna el menú completo"""
    menu_data = load_menu()
    return jsonify(menu_data)

@app.route('/ticket/<table_number>', methods=['GET'])
def get_ticket(table_number):
    """Obtiene el ticket actual de una mesa"""
    tickets_data = load_tickets()
    
    # Si no existe un ticket para esa mesa, devolver uno vacío
    if table_number not in tickets_data["tickets"]:
        return jsonify({
            "table": table_number,
            "items": [],
            "total": 0
        })
    
    return jsonify(tickets_data["tickets"][table_number])

@app.route('/ticket/<table_number>', methods=['POST'])
def update_ticket(table_number):
    """Actualiza o crea un ticket para una mesa"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Datos inválidos'}), 400
    
    tickets_data = load_tickets()
    
    # Actualizar el ticket
    tickets_data["tickets"][table_number] = {
        "table": table_number,
        "items": data.get("items", []),
        "total": data.get("total", 0)
    }
    
    save_tickets(tickets_data)
    return jsonify({'success': True, 'ticket': tickets_data["tickets"][table_number]})

@app.route('/ticket/<table_number>/add_item', methods=['POST'])
def add_item_to_ticket(table_number):
    """Añade un artículo al ticket de una mesa"""
    data = request.json
    if not data or "item_id" not in data:
        return jsonify({'success': False, 'message': 'Datos inválidos'}), 400
    
    # Cargar el menú para obtener los detalles del ítem
    menu_data = load_menu()
    item = None
    
    # Buscar el ítem en el menú
    for category in menu_data["categories"]:
        for menu_item in category["items"]:
            if menu_item["id"] == data["item_id"]:
                item = menu_item
                break
        if item:
            break
    
    if not item:
        return jsonify({'success': False, 'message': 'Artículo no encontrado'}), 404
    
    # Cargar los tickets
    tickets_data = load_tickets()
    
    # Crear el ticket si no existe
    if table_number not in tickets_data["tickets"]:
        tickets_data["tickets"][table_number] = {
            "table": table_number,
            "items": [],
            "total": 0
        }
    
    # Añadir el ítem al ticket
    ticket_item = {
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "quantity": data.get("quantity", 1)
    }
    
    # Calcular el nuevo total
    tickets_data["tickets"][table_number]["items"].append(ticket_item)
    total = sum(item["price"] * item["quantity"] for item in tickets_data["tickets"][table_number]["items"])
    tickets_data["tickets"][table_number]["total"] = total
    
    save_tickets(tickets_data)
    return jsonify({'success': True, 'ticket': tickets_data["tickets"][table_number]})

@app.route('/ticket/<table_number>/remove_item', methods=['POST'])
def remove_item_from_ticket(table_number):
    """Elimina un artículo del ticket de una mesa"""
    data = request.json
    if not data or "item_index" not in data:
        return jsonify({'success': False, 'message': 'Datos inválidos'}), 400
    
    tickets_data = load_tickets()
    
    # Verificar que exista el ticket
    if table_number not in tickets_data["tickets"]:
        return jsonify({'success': False, 'message': 'Ticket no encontrado'}), 404
    
    # Verificar que existe el ítem en el índice especificado
    if data["item_index"] < 0 or data["item_index"] >= len(tickets_data["tickets"][table_number]["items"]):
        return jsonify({'success': False, 'message': 'Índice de artículo inválido'}), 400
    
    # Eliminar el ítem
    tickets_data["tickets"][table_number]["items"].pop(data["item_index"])
    
    # Recalcular el total
    total = sum(item["price"] * item["quantity"] for item in tickets_data["tickets"][table_number]["items"])
    tickets_data["tickets"][table_number]["total"] = total
    
    save_tickets(tickets_data)
    return jsonify({'success': True, 'ticket': tickets_data["tickets"][table_number]})

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    init_db()  # Initialize database on startup
    app.run(debug=True, host='0.0.0.0', port=5002) 