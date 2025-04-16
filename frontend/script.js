document.addEventListener('DOMContentLoaded', function() {
    // Espera a que el contenido del DOM esté completamente cargado antes de ejecutar el código

    // Configuration
    const API_URL = 'http://localhost:5002/verify_pin'; // URL del endpoint para verificar el PIN
    const TEST_URL = 'http://localhost:5002/test-cors'; // URL del endpoint para probar CORS
    const KITCHEN_URL = 'http://localhost:5002/ticket'; // URL base para operaciones de tickets
    const MAX_PIN_LENGTH = 4; // Longitud máxima del PIN
    
    // DOM Elements
    const keys = document.querySelectorAll('.key[data-value]'); // Selecciona todos los botones de dígitos
    const clearBtn = document.getElementById('clear-btn'); // Botón para limpiar el PIN ingresado
    const submitBtn = document.getElementById('submit-btn'); // Botón para enviar el PIN
    const resetBtn = document.getElementById('reset-btn'); // Botón para reiniciar la entrada
    const pinDots = document.querySelectorAll('.pin-dot'); // Selecciona los puntos que representan el PIN ingresado
    const resultContainer = document.getElementById('result-container'); // Contenedor para mostrar el resultado
    const employeeNameElement = document.getElementById('employee-name'); // Elemento para mostrar el nombre del empleado
    const messageArea = document.getElementById('message-area'); // Área para mostrar mensajes de estado
    
    // Prueba inicial de conexión
    testBackendConnection(); // Llama a la función para probar la conexión con el backend
    
    // State
    let currentPin = ''; // Variable para almacenar el PIN ingresado
    
    // Event Listeners
    keys.forEach(key => {
        // Agrega un evento de clic a cada botón de dígito
        key.addEventListener('click', () => addDigit(key.getAttribute('data-value'))); // Llama a addDigit con el valor del botón
    });
    
    clearBtn.addEventListener('click', clearPin); // Agrega un evento de clic al botón de limpiar
    submitBtn.addEventListener('click', submitPin); // Agrega un evento de clic al botón de enviar
    resetBtn.addEventListener('click', reset); // Agrega un evento de clic al botón de reiniciar
    
    // Add keyboard support
    document.addEventListener('keydown', (e) => {
        // Agrega un evento de teclado para manejar la entrada del PIN
        if (e.key >= '0' && e.key <= '9' && currentPin.length < MAX_PIN_LENGTH) {
            // Si la tecla presionada es un dígito y el PIN no ha alcanzado su longitud máxima
            addDigit(e.key); // Llama a addDigit con el dígito presionado
        } else if (e.key === 'Backspace') {
            clearPin(); // Si se presiona Backspace, limpia el PIN
        } else if (e.key === 'Enter') {
            submitPin(); // Si se presiona Enter, envía el PIN
        }
    });
    
    // Función para probar la conexión con el backend
    async function testBackendConnection() {
        try {
            console.log("Prueba de conexión al backend iniciada..."); // Mensaje de inicio de prueba
            
            // Primero, prueba la ruta de prueba CORS
            console.log("Probando la ruta /test-cors..."); // Mensaje de prueba de CORS
            const testResponse = await fetch(TEST_URL, {
                method: 'GET', // Método de la solicitud
                headers: {
                    'Accept': 'application/json' // Espera una respuesta en formato JSON
                },
                mode: 'cors' // Habilita CORS
            }).catch(error => {
                console.error("Error al conectar con /test-cors:", error); // Manejo de errores
                return null; // Retorna null en caso de error
            });
            
            if (testResponse) {
                console.log("Respuesta de /test-cors recibida:", testResponse.status); // Muestra el estado de la respuesta
                if (testResponse.ok) {
                    const testData = await testResponse.json(); // Parsea la respuesta JSON
                    console.log("Datos de /test-cors:", testData); // Muestra los datos recibidos
                    console.log("✅ Conexión CORS básica funciona correctamente"); // Mensaje de éxito
                } else {
                    console.warn("❌ La prueba de CORS falló con estado:", testResponse.status); // Mensaje de advertencia
                }
            } else {
                console.warn("❌ No se pudo conectar con la ruta /test-cors"); // Mensaje de advertencia si no hay respuesta
            }
            
            // Ahora, intentamos una solicitud OPTIONS a verify_pin
            console.log("Probando solicitud OPTIONS a /verify_pin..."); // Mensaje de prueba de OPTIONS
            const optionsResponse = await fetch(API_URL, {
                method: 'OPTIONS', // Método de la solicitud
                headers: {
                    'Accept': 'application/json', // Espera una respuesta en formato JSON
                    'Content-Type': 'application/json' // Indica que el contenido es JSON
                },
                mode: 'cors' // Habilita CORS
            }).catch(error => {
                console.error("Error al realizar solicitud OPTIONS:", error); // Manejo de errores
                return null; // Retorna null en caso de error
            });
            
            if (optionsResponse) {
                console.log("Respuesta OPTIONS recibida:", optionsResponse.status); // Muestra el estado de la respuesta
                console.log("Headers OPTIONS:", [...optionsResponse.headers.entries()]); // Muestra las cabeceras de la respuesta
                console.log("✅ Solicitud OPTIONS procesada correctamente"); // Mensaje de éxito
            } else {
                console.warn("❌ La solicitud OPTIONS falló"); // Mensaje de advertencia si no hay respuesta
            }
        } catch (error) {
            console.error("Error general en prueba de conexión:", error); // Manejo de errores generales
        }
    }
    
    // Functions
    function addDigit(digit) {
        // Agrega un dígito al PIN actual
        if (currentPin.length < MAX_PIN_LENGTH) {
            // Si el PIN actual no ha alcanzado su longitud máxima
            currentPin += digit; // Agrega el dígito al PIN
            updatePinDisplay(); // Actualiza la visualización del PIN
            
            // Automatically submit when PIN is complete
            if (currentPin.length === MAX_PIN_LENGTH) {
                setTimeout(submitPin, 300); // Envía el PIN automáticamente después de 300 ms si está completo
            }
        }
    }
    
    function clearPin() {
        // Limpia el PIN actual
        currentPin = ''; // Reinicia el PIN
        updatePinDisplay(); // Actualiza la visualización del PIN
        messageArea.textContent = ''; // Limpia el área de mensajes
    }
    
    function updatePinDisplay() {
        // Actualiza la visualización de los puntos del PIN
        pinDots.forEach((dot, index) => {
            // Itera sobre cada punto
            if (index < currentPin.length) {
                dot.classList.add('filled'); // Agrega la clase 'filled' si el índice es menor que la longitud del PIN
            } else {
                dot.classList.remove('filled'); // Elimina la clase 'filled' si el índice es mayor o igual
            }
        });
    }
    
    async function submitPin() {
        // Envía el PIN al backend para verificación
        if (currentPin.length !== MAX_PIN_LENGTH) {
            messageArea.textContent = 'Por favor ingrese un PIN de 4 dígitos'; // Mensaje de error si el PIN no es válido
            return; // Sale de la función
        }
        
        try {
            messageArea.textContent = 'Verificando...'; // Mensaje de verificación
            
            console.log("Enviando solicitud al backend:", { pin: currentPin }); // Muestra el PIN que se está enviando
            console.log("URL:", API_URL); // Muestra la URL del backend
            console.log("Método:", "POST"); // Muestra el método de la solicitud
            
            // Usar XMLHttpRequest para obtener más información sobre los errores
            const xhr = new XMLHttpRequest(); // Crea una nueva instancia de XMLHttpRequest
            xhr.open('POST', API_URL, true); // Configura la solicitud POST
            xhr.setRequestHeader('Content-Type', 'application/json'); // Establece el tipo de contenido
            xhr.setRequestHeader('Accept', 'application/json'); // Establece el tipo de respuesta esperada
            
            xhr.onload = function() {
                // Maneja la respuesta de la solicitud
                console.log("XHR respuesta recibida. Estado:", xhr.status); // Muestra el estado de la respuesta
                console.log("Respuesta:", xhr.responseText); // Muestra el texto de la respuesta
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    // Si la respuesta es exitosa
                    try {
                        const data = JSON.parse(xhr.responseText); // Parsea la respuesta JSON
                        console.log("Datos parseados:", data); // Muestra los datos parseados
                        
                        if (data.success) {
                            // Si la verificación del PIN fue exitosa
                            // Store employee data in localStorage
                            const employeeData = {
                                name: data.employee.name, // Almacena el nombre del empleado
                                role: data.employee.role // Almacena el rol del empleado
                            };
                            localStorage.setItem('employeeData', JSON.stringify(employeeData)); // Guarda los datos en localStorage
                            
                            // Check employee role for redirection
                            if (data.employee.role === 'Mesero') {
                                window.location.href = 'mesas.html'; // Redirige a la página de selección de mesas
                            } else {
                                // For other roles, show the traditional UI
                                employeeNameElement.textContent = data.employee.name; // Muestra el nombre del empleado
                                resultContainer.classList.add('show'); // Muestra el contenedor de resultados
                                messageArea.textContent = ''; // Limpia el área de mensajes
                            }
                        } else {
                            // PIN is invalid
                            messageArea.textContent = data.message || 'Error al verificar el PIN'; // Muestra el mensaje de error
                            clearPin(); // Limpia el PIN
                        }
                    } catch (e) {
                        console.error("Error al parsear respuesta JSON:", e); // Manejo de errores al parsear JSON
                        messageArea.textContent = 'Error al procesar la respuesta del servidor.'; // Mensaje de error
                        clearPin(); // Limpia el PIN
                    }
                } else {
                    console.error("Error en la solicitud. Estado:", xhr.status); // Manejo de errores de solicitud
                    messageArea.textContent = `Error en la solicitud (${xhr.status}). Intente nuevamente.`; // Mensaje de error
                    clearPin(); // Limpia el PIN
                }
            };
            
            xhr.onerror = function() {
                console.error("Error de red en la solicitud XHR"); // Manejo de errores de red
                messageArea.textContent = 'Error de conexión. Intente nuevamente.'; // Mensaje de error
                clearPin(); // Limpia el PIN
            };
            
            xhr.send(JSON.stringify({ pin: currentPin })); // Envía el PIN como JSON al backend
            
        } catch (error) {
            console.error('Error general:', error); // Manejo de errores generales
            messageArea.textContent = 'Error de conexión. Intente nuevamente. Asegúrate de que el servidor backend esté en ejecución.'; // Mensaje de error
            clearPin(); // Limpia el PIN
        }
    }
    
    function reset() {
        // Reinicia el estado de la interfaz
        currentPin = ''; // Reinicia el PIN
        updatePinDisplay(); // Actualiza la visualización del PIN
        resultContainer.classList.remove('show'); // Oculta el contenedor de resultados
        messageArea.textContent = ''; // Limpia el área de mensajes
    }
    
    // Función para confirmar y enviar el ticket a la cocina
    window.confirmAndSendTicket = function(tableNumber) {
        if (!tableNumber) {
            alert('Número de mesa no especificado');
            return;
        }
        
        try {
            // Mostrar mensaje de carga
            if (messageArea) {
                messageArea.textContent = 'Enviando ticket a cocina...';
            }
            
            fetch(`${KITCHEN_URL}/${tableNumber}/confirm`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error de servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Ticket enviado correctamente
                    alert('Ticket enviado a cocina correctamente');
                    
                    // Si hay un área de mensajes, actualizar
                    if (messageArea) {
                        messageArea.textContent = 'Ticket enviado exitosamente';
                    }
                    
                    // Puedes redirigir a otra página o realizar otras acciones aquí
                    console.log('Ticket confirmado:', data.ticket);
                } else {
                    // Error al enviar el ticket
                    alert(`Error: ${data.message}`);
                    if (messageArea) {
                        messageArea.textContent = `Error: ${data.message}`;
                    }
                }
            })
            .catch(error => {
                console.error('Error al confirmar ticket:', error);
                alert(`Error de conexión: ${error.message}`);
                
                if (messageArea) {
                    messageArea.textContent = `Error de conexión: ${error.message}`;
                }
            });
        } catch (error) {
            console.error('Error general:', error);
            alert(`Error: ${error.message}`);
        }
    };
}); 