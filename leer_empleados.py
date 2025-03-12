import sqlite3

# Ruta a la base de datos
DATABASE_PATH = 'backend/employees.db'      

def read_employees():
    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Ejecutar la consulta
    cursor.execute('SELECT * FROM employees')
    
    # Obtener todos los resultados
    employees = cursor.fetchall()
    
    # Imprimir los resultados
    for employee in employees:
        print(f'ID: {employee[0]}, PIN: {employee[1]}, Nombre: {employee[2]}')
    
    # Cerrar la conexión
    conn.close()

def update_employee_name(employee_id, new_name):
    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Ejecutar la consulta de actualización
    cursor.execute('UPDATE employees SET name = ? WHERE id = ?', (new_name, employee_id))
    
    # Confirmar los cambios
    conn.commit()
    
    # Cerrar la conexión
    conn.close()
    print(f'Nombre del empleado con ID {employee_id} actualizado a {new_name}.')

# Llamar a la función para leer empleados
read_employees()
    