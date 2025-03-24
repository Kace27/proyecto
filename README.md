<<<<<<< HEAD
# Sistema de Verificación de PIN

Esta aplicación permite a los empleados ingresar un PIN de 4 dígitos para identificarse en el sistema.

## Estructura del Proyecto

```
proyecto/
├── backend/
│   ├── app.py              # Aplicación Flask (backend)
│   └── requirements.txt    # Dependencias de Python
├── frontend/
│   ├── index.html          # Estructura HTML
│   ├── style.css           # Estilos CSS
│   ├── script.js           # Lógica JavaScript
│   └── server.py           # Servidor web simple para el frontend
├── venv/                   # Entorno virtual (no incluido en repositorio)
├── run.sh                  # Script para ejecutar la aplicación
└── README.md               # Este archivo
```

## Requisitos

- Python 3.7 o superior
- Navegador web moderno (Chrome, Firefox, Edge, etc.)

## Configuración y Ejecución

### Configuración del Entorno Virtual

1. Crea un entorno virtual (solo necesitas hacerlo una vez):
   ```
   python -m venv venv
   ```

2. Activa el entorno virtual:
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - En Windows:
     ```
     venv\Scripts\activate
     ```

3. Instala las dependencias:
   ```
   pip install -r backend/requirements.txt
   ```

### Ejecución Rápida (Recomendado)

Para iniciar tanto el servidor backend como el frontend, usa el script incluido:

```
./run.sh
```

O, alternativamente:

```
bash run.sh
```

Luego abre en tu navegador: **http://localhost:8000**

### Ejecución Manual (Avanzado)

Si prefieres ejecutar los servidores manualmente:

1. **Backend**:
   ```
   cd backend
   python app.py
   ```
   El servidor Flask se iniciará en http://localhost:5000.

2. **Frontend**:
   ```
   cd frontend
   python server.py
   ```
   El servidor frontend se iniciará en http://localhost:8000.

   **Importante**: Para evitar problemas de CORS, es recomendable acceder a la aplicación a través del servidor web (http://localhost:8000) en lugar de abrir el archivo HTML directamente.

## Solución de Problemas de CORS

Si encuentras errores relacionados con CORS (Cross-Origin Resource Sharing), asegúrate de:

1. Usar el servidor web para el frontend (http://localhost:8000) en lugar de abrir el archivo HTML directamente.
2. Verificar que el servidor backend (Flask) esté en ejecución.
3. Comprobar que ambos servidores estén ejecutándose en los puertos correctos (5000 para backend, 8000 para frontend).

## Uso

1. El sistema muestra un teclado numérico para ingresar el PIN.
2. Ingresa un PIN de 4 dígitos.
3. Si el PIN es válido, se mostrará el nombre del empleado correspondiente.
4. Si el PIN es inválido, se mostrará un mensaje de error.

## Datos de Prueba

La aplicación viene preconfigurada con los siguientes PINs:

- PIN: 1234 - Nombre: Juan Pérez
- PIN: 5678 - Nombre: Ana García
- PIN: 9012 - Nombre: Carlos Rodríguez
- PIN: 4321 - Nombre: María López
- PIN: 8765 - Nombre: Pedro Sánchez 
=======