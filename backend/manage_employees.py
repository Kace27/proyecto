#!/usr/bin/env python3
import json
import os
import sys

# Ruta al archivo JSON
DATABASE_PATH = 'employees.json'

def load_employees():
    """Carga los empleados desde el archivo JSON"""
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: El archivo JSON está mal formado")
            return {"employees": []}
    else:
        print(f"Aviso: No se encontró el archivo {DATABASE_PATH}, se creará uno nuevo")
        return {"employees": []}

def save_employees(data):
    """Guarda los empleados en el archivo JSON"""
    with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Datos guardados en {DATABASE_PATH}")

def list_employees():
    """Lista todos los empleados"""
    data = load_employees()
    
    if not data["employees"]:
        print("No hay empleados registrados")
        return
    
    print("\n=== LISTA DE EMPLEADOS ===")
    print(f"{'ID':<5} {'PIN':<8} {'NOMBRE':<25} {'ROL':<15}")
    print("-" * 55)
    
    for emp in data["employees"]:
        print(f"{emp['id']:<5} {emp['pin']:<8} {emp['name']:<25} {emp['role']:<15}")
    
    print("-" * 55)
    print(f"Total: {len(data['employees'])} empleados")

def add_employee(pin, name, role):
    """Agrega un nuevo empleado"""
    if len(pin) != 4 or not pin.isdigit():
        print("Error: El PIN debe tener 4 dígitos")
        return False
    
    data = load_employees()
    
    # Verificar que el PIN no esté en uso
    if any(emp["pin"] == pin for emp in data["employees"]):
        print(f"Error: El PIN {pin} ya está en uso")
        return False
    
    # Asignar un nuevo ID (el máximo actual + 1)
    new_id = max([emp["id"] for emp in data["employees"]], default=0) + 1
    
    # Crear el nuevo empleado
    new_employee = {
        "id": new_id,
        "pin": pin,
        "name": name,
        "role": role
    }
    
    # Agregar a la lista de empleados
    data["employees"].append(new_employee)
    save_employees(data)
    
    print(f"Empleado agregado con éxito: {name} (ID: {new_id}, PIN: {pin}, Rol: {role})")
    return True

def update_employee(employee_id, **kwargs):
    """Actualiza la información de un empleado"""
    data = load_employees()
    
    # Buscar el empleado con el ID correspondiente
    employee_index = next((i for i, emp in enumerate(data["employees"]) if emp["id"] == employee_id), None)
    
    if employee_index is None:
        print(f"Error: No se encontró un empleado con ID {employee_id}")
        return False
    
    employee = data["employees"][employee_index]
    updated = False
    
    # Actualizar PIN
    if "pin" in kwargs and kwargs["pin"]:
        pin = kwargs["pin"]
        if len(pin) != 4 or not pin.isdigit():
            print("Error: El PIN debe tener 4 dígitos")
            return False
        
        # Verificar que el PIN no esté en uso por otro empleado
        if any(emp["pin"] == pin and emp["id"] != employee_id for emp in data["employees"]):
            print(f"Error: El PIN {pin} ya está en uso por otro empleado")
            return False
        
        employee["pin"] = pin
        updated = True
    
    # Actualizar nombre
    if "name" in kwargs and kwargs["name"]:
        employee["name"] = kwargs["name"]
        updated = True
    
    # Actualizar rol
    if "role" in kwargs and kwargs["role"]:
        employee["role"] = kwargs["role"]
        updated = True
    
    if updated:
        save_employees(data)
        print(f"Empleado actualizado con éxito (ID: {employee_id}):")
        print(f"PIN: {employee['pin']}")
        print(f"Nombre: {employee['name']}")
        print(f"Rol: {employee['role']}")
        return True
    else:
        print("No se realizaron cambios")
        return False

def delete_employee(employee_id):
    """Elimina un empleado"""
    data = load_employees()
    
    # Buscar el empleado con el ID correspondiente
    employee_index = next((i for i, emp in enumerate(data["employees"]) if emp["id"] == employee_id), None)
    
    if employee_index is None:
        print(f"Error: No se encontró un empleado con ID {employee_id}")
        return False
    
    # Guardar el nombre para el mensaje de confirmación
    employee_name = data["employees"][employee_index]["name"]
    
    # Eliminar el empleado
    data["employees"].pop(employee_index)
    save_employees(data)
    
    print(f"Empleado eliminado con éxito: {employee_name} (ID: {employee_id})")
    return True

def print_help():
    """Muestra la ayuda del script"""
    print("""
Uso: python manage_employees.py <comando> [opciones]

Comandos disponibles:
  list                     Lista todos los empleados
  add <pin> <name> <role>  Agrega un nuevo empleado
  update <id> [opciones]   Actualiza un empleado existente
  delete <id>              Elimina un empleado

Opciones para 'update':
  --pin=<pin>              Nuevo PIN (4 dígitos)
  --name=<name>            Nuevo nombre
  --role=<role>            Nuevo rol

Ejemplos:
  python manage_employees.py list
  python manage_employees.py add 1234 "Juan Pérez" Mesero
  python manage_employees.py update 1 --name="Juan García" --role=Gerente
  python manage_employees.py delete 1
    """)

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_employees()
    
    elif command == "add":
        if len(sys.argv) < 5:
            print("Error: Faltan argumentos para 'add'")
            print("Uso: python manage_employees.py add <pin> <name> <role>")
            return
        
        pin = sys.argv[2]
        name = sys.argv[3]
        role = sys.argv[4]
        add_employee(pin, name, role)
    
    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: Faltan argumentos para 'update'")
            print("Uso: python manage_employees.py update <id> [opciones]")
            return
        
        try:
            employee_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: El ID debe ser un número entero")
            return
        
        kwargs = {}
        for arg in sys.argv[3:]:
            if arg.startswith("--pin="):
                kwargs["pin"] = arg.split("=", 1)[1]
            elif arg.startswith("--name="):
                kwargs["name"] = arg.split("=", 1)[1]
            elif arg.startswith("--role="):
                kwargs["role"] = arg.split("=", 1)[1]
        
        update_employee(employee_id, **kwargs)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Faltan argumentos para 'delete'")
            print("Uso: python manage_employees.py delete <id>")
            return
        
        try:
            employee_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: El ID debe ser un número entero")
            return
        
        delete_employee(employee_id)
    
    else:
        print(f"Error: Comando desconocido '{command}'")
        print_help()

if __name__ == "__main__":
    main() 