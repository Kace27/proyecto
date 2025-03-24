# Especificaciones del Sistema de Gestión de Restaurante

## Descripción General
El sistema está diseñado para la gestión de operaciones en un restaurante, permitiendo la identificación de empleados mediante PIN, gestión de mesas, creación de tickets (órdenes) y administración del menú. La aplicación consta de un frontend web y un backend API desarrollado con Flask.

## Objetivos del Sistema
- Permitir la autenticación de empleados mediante PIN
- Gestionar la asignación y estado de mesas
- Crear y modificar tickets (órdenes) para cada mesa
- Administrar el menú de productos
- Facilitar las operaciones diarias del restaurante

## Arquitectura Técnica

### Stack Tecnológico
- **Backend**: Python con Flask, sistema de almacenamiento basado en archivos JSON
- **Frontend**: HTML, CSS y JavaScript vanilla
- **Comunicación**: API REST

### Componentes del Sistema
1. **Sistema de Autenticación**
   - Verificación de PINs de empleados
   - Gestión de sesiones
   - Roles de usuarios (Mesero, Gerente, Administrador, Cocina)

2. **Gestión de Mesas**
   - Visualización del estado de mesas
   - Asignación de mesas
   - Indicador visual de mesas ocupadas/libres

3. **Sistema de Tickets**
   - Creación de nuevos tickets asociados a mesas
   - Adición y eliminación de productos al ticket
   - Cálculo de totales
   - Gestión del estado del ticket

4. **Gestión del Menú**
   - Categorización de productos
   - Información de productos (nombre, precio, imagen)
   - Interfaz para selección de productos

## Funcionalidades Principales

### Módulo de Autenticación
- Ingreso de PIN de 4 dígitos
- Verificación contra base de datos
- Redirección a interfaz de mesas tras autenticación exitosa
- Gestión de sesión del empleado

### Módulo de Mesas
- Visualización de todas las mesas del restaurante
- Mesas representadas gráficamente con indicadores de estado
- Navegación a tickets específicos de mesa seleccionada

### Módulo de Tickets
- Creación de ticket asociado a una mesa
- Interfaz para añadir/eliminar productos al ticket
- Organización del menú por categorías
- Cálculo automático de totales
- Gestión del estado del ticket (en proceso, completado, etc.)

### Módulo de Administración (Backend)
- Gestión de empleados (alta, baja, modificación)
- Gestión del menú (categorías, productos)
- Reportes y estadísticas

## Almacenamiento de Datos
El sistema utiliza archivos JSON como mecanismo de persistencia:
- `employees.json`: Almacena información de empleados (ID, PIN, nombre, rol)
- `tickets.json`: Almacena los tickets/órdenes por mesa
- `menu.json`: Almacena las categorías y productos del menú

## Interfaz de Usuario
- Diseño responsivo adaptado a diferentes dispositivos
- Interfaz intuitiva con elementos gráficos para facilitar la operación
- Flujo de trabajo optimizado para operaciones rápidas

## Restricciones y Consideraciones
- El sistema está diseñado para funcionar en entorno local
- Se requiere Python 3.7 o superior
- Navegadores web modernos (Chrome, Firefox, Edge, etc.)
- Para evitar problemas CORS, se debe acceder a través del servidor web frontend

## Procedimiento de Instalación y Ejecución
1. Crear y activar entorno virtual
2. Instalar dependencias (`pip install -r backend/requirements.txt`)
3. Ejecutar script de inicio (`./run.sh` o `bash run.sh`)
4. Acceder a la aplicación: http://localhost:8000

## Análisis a Nivel de Componentes, Objetos, Clases y Métodos

### Componentes Principales

#### 1. Frontend
- **Páginas HTML**: 
  - `index.html`: Interfaz de autenticación mediante PIN
  - `mesas.html`: Visualización y selección de mesas
  - `ticket.html`: Gestión de tickets y selección de productos

- **Estilos**:
  - `style.css`: Estilos compartidos entre las diferentes vistas

- **Lógica JS**:
  - `script.js`: Manejo de eventos, comunicación con API, manipulación del DOM

#### 2. Backend (Flask)
- **API REST**: Implementada en `app.py`
- **Modelos de datos**: Gestionados mediante archivos JSON

### Objetos y Clases Principales

#### Objetos de Datos:
1. **Empleado**:
   - Atributos: id, pin, name, role
   - Operaciones: verificación, actualización, creación

2. **Mesa**:
   - Atributos: número, estado (libre/ocupada)
   - Operaciones: cambio de estado, asignación a empleado

3. **Ticket**:
   - Atributos: mesa asociada, items, total, estado
   - Operaciones: añadir/eliminar items, calcular total

4. **Item de Menú**:
   - Atributos: id, nombre, precio, imagen, categoría
   - Operaciones: añadir a ticket

#### Métodos Principales del Backend:

1. **Gestión de Autenticación**:
   - `verify_pin()`: Verifica el PIN de un empleado
   
2. **Gestión de Empleados**:
   - `get_employees()`: Obtiene lista de empleados
   - `add_employee()`: Añade un nuevo empleado
   - `update_employee()`: Actualiza información de un empleado

3. **Gestión de Menú**:
   - `get_menu()`: Obtiene el menú completo con categorías

4. **Gestión de Tickets**:
   - `get_ticket()`: Obtiene el ticket de una mesa específica
   - `update_ticket()`: Actualiza información de un ticket
   - `add_item_to_ticket()`: Añade un item al ticket
   - `remove_item_from_ticket()`: Elimina un item del ticket

5. **Gestión de Datos**:
   - `load_employees()`: Carga datos de empleados desde JSON
   - `save_employees()`: Guarda datos de empleados en JSON
   - `load_tickets()`: Carga datos de tickets desde JSON
   - `save_tickets()`: Guarda datos de tickets en JSON
   - `load_menu()`: Carga datos del menú desde JSON
   - `save_menu()`: Guarda datos del menú en JSON
   - `init_db()`: Inicializa la base de datos si no existe

### Interacción entre Componentes

1. **Flujo de Autenticación**:
   - Frontend: Captura PIN en `index.html`
   - JS: Envía solicitud a API en `script.js`
   - Backend: Verifica PIN en `verify_pin()`
   - Frontend: Redirige a `mesas.html` si es correcto

2. **Flujo de Gestión de Tickets**:
   - Usuario selecciona mesa en `mesas.html`
   - JS: Redirige a `ticket.html` con número de mesa
   - Backend: `get_ticket()` obtiene o crea ticket para la mesa
   - Usuario: Interactúa con interfaz para añadir/eliminar items
   - Backend: Actualiza ticket mediante `add_item_to_ticket()` y `remove_item_from_ticket()`

### Patrones de Diseño Observados

1. **MVC Simplificado**:
   - Modelo: Archivos JSON y funciones de manipulación
   - Vista: Archivos HTML y CSS
   - Controlador: API Flask y lógica JavaScript

2. **API REST**:
   - Endpoints bien definidos para cada recurso
   - Métodos HTTP según operación (GET, POST, PUT)
   - Respuestas en formato JSON

3. **Persistencia Simple**:
   - Uso de archivos JSON como base de datos
   - Funciones de carga/guardado para cada tipo de dato

Este sistema está diseñado con una arquitectura desacoplada que separa claramente el frontend del backend, facilitando el mantenimiento y la escalabilidad futura, aunque con un enfoque pragmático utilizando almacenamiento basado en archivos JSON en lugar de una base de datos relacional tradicional.
