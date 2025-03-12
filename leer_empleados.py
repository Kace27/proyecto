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

# Llamar a la función
read_employees()