#!/bin/bash

# Activar el entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar que el entorno virtual está activado
echo "Usando Python: $(which python)"

# Matar cualquier proceso existente que use los puertos 5000 y 8000
echo "Verificando y matando procesos que utilizan los puertos 5000 y 8000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Lanzar el backend
echo "Iniciando servidor Flask (backend) en http://localhost:5000..."
cd backend
FLASK_DEBUG=1 python app.py &
BACKEND_PID=$!

# Esperar a que el backend esté listo
echo "Esperando a que el backend esté listo..."
sleep 2

# Verificar que el backend esté ejecutándose
if ! curl -s http://localhost:5000/test-cors > /dev/null; then
    echo "⚠️ Advertencia: No se pudo conectar con el backend. Verificar logs."
else
    echo "✅ Backend está respondiendo correctamente."
fi

# Volver al directorio principal
cd ..

# Lanzar el frontend
echo "Iniciando servidor frontend en http://localhost:8000..."
cd frontend
python server.py &
FRONTEND_PID=$!

# Dar tiempo para que se inicien los servidores
sleep 2

echo ""
echo "Ambos servidores están ejecutándose."
echo "- Backend: http://localhost:5000"
echo "- Frontend: http://localhost:8000"
echo ""
echo "Para probar la aplicación, abre uno de estos enlaces en tu navegador:"
echo "- http://localhost:8000/index.html (Recomendado)"
echo "- http://localhost:8000/ (Si el anterior no funciona)"
echo ""
echo "Para probar directamente la conexión CORS:"
echo "- http://localhost:5000/test-cors (Debe devolver un mensaje JSON)"
echo ""
echo "Presiona Ctrl+C para detener los servidores."

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Atrapar la señal de interrupción para limpiar
trap cleanup INT

# Mostrar los logs del backend para depuración
echo ""
echo "Mostrando logs del backend (espera unos segundos y presiona Ctrl+C para detener):"
echo ""
tail -f backend/app.log &
LOG_PID=$!

# Esperar a que termine uno de los procesos
wait $BACKEND_PID $FRONTEND_PID
kill $LOG_PID 2>/dev/null 