### Product Backlog
#### Módulo de Autenticación

1. **Ingreso de PIN de 4 dígitos**
   - Implementar la interfaz de usuario para la entrada del PIN.
   - Desarrollar la lógica para verificar el PIN contra la base de datos.
   - Redirigir a la interfaz de mesas tras autenticación exitosa.
   - Implementar gestión de sesión del empleado.

#### Módulo de Mesas
2. **Visualización de Mesas**
   - Crear una interfaz gráfica que muestre todas las mesas del restaurante.
   - Implementar indicadores visuales para el estado de las mesas (ocupadas/libres).
   - Permitir la asignación de mesas a empleados.

3. **Navegación a Tickets**
   - Implementar la funcionalidad para navegar a tickets específicos de la mesa seleccionada.

#### Módulo de Tickets
4. **Creación de Tickets**
   - Desarrollar la interfaz para crear un nuevo ticket asociado a una mesa.
   - Implementar la lógica para añadir y eliminar productos del ticket.
   - Calcular automáticamente el total del ticket.

5. **Gestión del Estado del Ticket**
   - Implementar la gestión del estado del ticket.

6. **Personalización de Artículos**
   - Desarrollar la interfaz modal para la personalización de artículos.
   - Implementar la selección de variantes (A, B, C) para cada artículo.
   - Permitir la activación/desactivación de ingredientes específicos.
   - Visualizar ingredientes con potencial alérgeno.

#### Módulo de Gestión del Menú
7. **Administración del Menú**
   - Crear una interfaz para la categorización de productos.
   - Implementar la visualización de información de productos (nombre, precio, imagen).
   - Desarrollar la lógica para la selección de productos.


#### Almacenamiento de Datos
11. **Persistencia de Datos**
    - Implementar la carga y guardado de datos en archivos JSON:
      - `employees.json`: Información de empleados.
      - `tickets.json`: Tickets/órdenes por mesa.
      - `menu.json`: Categorías y productos del menú.

#### Interfaz de Usuario
12. **Diseño Responsivo**~~
    - Asegurar que la interfaz sea responsiva y se adapte a diferentes dispositivos.
    - Optimizar el flujo de trabajo para operaciones rápidas.

#### Modulo Chef
13. **Gestión Pantalla de Cocina**
    - Muestra los articulos del ticket que envia el mesero
    - Implemeta la lógica para marcar como completado un articulo y un ticket 

### Consideraciones Adicionales
- **Pruebas y Validación**
  - Implementar pruebas unitarias y de integración para asegurar la funcionalidad del sistema.
- **Mantenimiento y Escalabilidad**
  - Planificar la arquitectura para facilitar el mantenimiento y la escalabilidad futura.
