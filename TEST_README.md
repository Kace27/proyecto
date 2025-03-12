# Prueba de Conexión Frontend-Backend

Este script permite probar la conexión entre el frontend y el backend de la aplicación de Verificación de PIN.

## Características

- Inicia automáticamente tanto el servidor backend (Flask) como el servidor frontend
- Prueba la comunicación con el endpoint `/verify_pin`
- Abre el navegador automáticamente con la interfaz de usuario
- Verifica la existencia de la base de datos y la crea si es necesario
- Permite especificar puertos personalizados para los servidores

## Requisitos

Antes de usar este script, asegúrate de tener instaladas todas las dependencias:

```bash
source venv/bin/activate  # Activa el entorno virtual
pip install -r backend/requirements.txt
```

## Uso

### Ejecución básica

Para usar el script con la configuración predeterminada:

```bash
python test_connection.py
```

Esto iniciará:
- El servidor backend en el puerto 5000
- El servidor frontend en el puerto 8000

### Personalización de puertos

Si necesitas usar puertos diferentes:

```bash
python test_connection.py --port 5001 --frontend-port 8080
```

## ¿Qué hace este script?

1. **Verifica la estructura del proyecto**:
   - Comprueba que existan las carpetas `backend` y `frontend`

2. **Verifica/crea la base de datos**:
   - Si no existe `backend/employees.db`, la crea con datos de ejemplo

3. **Inicia los servidores**:
   - Inicia el servidor Flask (backend)
   - Inicia el servidor HTTP simple para el frontend

4. **Prueba la conexión**:
   - Envía una solicitud POST al endpoint `/verify_pin` con un PIN de ejemplo (1234)
   - Verifica que la respuesta sea correcta

5. **Abre el navegador**:
   - Si la prueba de conexión es exitosa, abre el navegador con la URL del frontend

6. **Limpieza**:
   - Al presionar Enter, detiene ambos servidores correctamente

## Solución de problemas

Si encuentras errores al ejecutar el script:

1. **Error de puerto en uso**:
   - Usa los parámetros `--port` y `--frontend-port` para especificar puertos diferentes

2. **Error de módulo no encontrado**:
   - Asegúrate de haber instalado todas las dependencias con `pip install -r backend/requirements.txt`

3. **Error de conexión rechazada**:
   - Verifica que no haya un firewall bloqueando las conexiones locales
   - Asegúrate de que no hay otros servicios usando los mismos puertos 