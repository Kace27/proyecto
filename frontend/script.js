document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const API_URL = 'http://localhost:5002/verify_pin';
    const TEST_URL = 'http://localhost:5002/test-cors';
    const MAX_PIN_LENGTH = 4;
    
    // DOM Elements
    const keys = document.querySelectorAll('.key[data-value]');
    const clearBtn = document.getElementById('clear-btn');
    const submitBtn = document.getElementById('submit-btn');
    const resetBtn = document.getElementById('reset-btn');
    const pinDots = document.querySelectorAll('.pin-dot');
    const resultContainer = document.getElementById('result-container');
    const employeeNameElement = document.getElementById('employee-name');
    const messageArea = document.getElementById('message-area');
    
    // Prueba inicial de conexión
    testBackendConnection();
    
    // State
    let currentPin = '';
    
    // Event Listeners
    keys.forEach(key => {
        key.addEventListener('click', () => addDigit(key.getAttribute('data-value')));
    });
    
    clearBtn.addEventListener('click', clearPin);
    submitBtn.addEventListener('click', submitPin);
    resetBtn.addEventListener('click', reset);
    
    // Add keyboard support
    document.addEventListener('keydown', (e) => {
        if (e.key >= '0' && e.key <= '9' && currentPin.length < MAX_PIN_LENGTH) {
            addDigit(e.key);
        } else if (e.key === 'Backspace') {
            clearPin();
        } else if (e.key === 'Enter') {
            submitPin();
        }
    });
    
    // Función para probar la conexión con el backend
    async function testBackendConnection() {
        try {
            console.log("Prueba de conexión al backend iniciada...");
            
            // Primero, prueba la ruta de prueba CORS
            console.log("Probando la ruta /test-cors...");
            const testResponse = await fetch(TEST_URL, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                },
                mode: 'cors'
            }).catch(error => {
                console.error("Error al conectar con /test-cors:", error);
                return null;
            });
            
            if (testResponse) {
                console.log("Respuesta de /test-cors recibida:", testResponse.status);
                if (testResponse.ok) {
                    const testData = await testResponse.json();
                    console.log("Datos de /test-cors:", testData);
                    console.log("✅ Conexión CORS básica funciona correctamente");
                } else {
                    console.warn("❌ La prueba de CORS falló con estado:", testResponse.status);
                }
            } else {
                console.warn("❌ No se pudo conectar con la ruta /test-cors");
            }
            
            // Ahora, intentamos una solicitud OPTIONS a verify_pin
            console.log("Probando solicitud OPTIONS a /verify_pin...");
            const optionsResponse = await fetch(API_URL, {
                method: 'OPTIONS',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                mode: 'cors'
            }).catch(error => {
                console.error("Error al realizar solicitud OPTIONS:", error);
                return null;
            });
            
            if (optionsResponse) {
                console.log("Respuesta OPTIONS recibida:", optionsResponse.status);
                console.log("Headers OPTIONS:", [...optionsResponse.headers.entries()]);
                console.log("✅ Solicitud OPTIONS procesada correctamente");
            } else {
                console.warn("❌ La solicitud OPTIONS falló");
            }
        } catch (error) {
            console.error("Error general en prueba de conexión:", error);
        }
    }
    
    // Functions
    function addDigit(digit) {
        if (currentPin.length < MAX_PIN_LENGTH) {
            currentPin += digit;
            updatePinDisplay();
            
            // Automatically submit when PIN is complete
            if (currentPin.length === MAX_PIN_LENGTH) {
                setTimeout(submitPin, 300);
            }
        }
    }
    
    function clearPin() {
        currentPin = '';
        updatePinDisplay();
        messageArea.textContent = '';
    }
    
    function updatePinDisplay() {
        // Update the PIN dots
        pinDots.forEach((dot, index) => {
            if (index < currentPin.length) {
                dot.classList.add('filled');
            } else {
                dot.classList.remove('filled');
            }
        });
    }
    
    async function submitPin() {
        if (currentPin.length !== MAX_PIN_LENGTH) {
            messageArea.textContent = 'Por favor ingrese un PIN de 4 dígitos';
            return;
        }
        
        try {
            messageArea.textContent = 'Verificando...';
            
            console.log("Enviando solicitud al backend:", { pin: currentPin });
            console.log("URL:", API_URL);
            console.log("Método:", "POST");
            
            // Usar XMLHttpRequest para obtener más información sobre los errores
            const xhr = new XMLHttpRequest();
            xhr.open('POST', API_URL, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('Accept', 'application/json');
            
            xhr.onload = function() {
                console.log("XHR respuesta recibida. Estado:", xhr.status);
                console.log("Respuesta:", xhr.responseText);
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        console.log("Datos parseados:", data);
                        
                        if (data.success) {
                            // Store employee data in localStorage
                            const employeeData = {
                                name: data.employee.name,
                                role: data.employee.role
                            };
                            localStorage.setItem('employeeData', JSON.stringify(employeeData));
                            
                            // Check employee role for redirection
                            if (data.employee.role === 'Mesero') {
                                // Redirect to table selection page
                                window.location.href = 'mesas.html';
                            } else {
                                // For other roles, show the traditional UI
                                employeeNameElement.textContent = data.employee.name;
                                resultContainer.classList.add('show');
                                messageArea.textContent = '';
                            }
                        } else {
                            // PIN is invalid
                            //messageArea.textContent = data.message || 'Error al verificar el PIN';
                            messageArea.textContent = 'PIN incorrecto. Ingrese un PIN válido';
                            messageArea.style.color = 'red';
                            clearPin();
                            setTimeout(() => {
                                messageArea.textContent = ''; // Clear message after 2 seconds
                            }, 2000);
                        }
                    } catch (e) {
                        console.error("Error al parsear respuesta JSON:", e);
                        messageArea.textContent = 'Error al procesar la respuesta del servidor.';
                        clearPin();
                    }
                } else {
                    console.error("Error en la solicitud. Estado:", xhr.status);
                    messageArea.textContent = `Error en la solicitud (${xhr.status}). Intente nuevamente.`;
                    clearPin();
                }
            };
            
            xhr.onerror = function() {
                console.error("Error de red en la solicitud XHR");
                messageArea.textContent = 'Error de conexión. Intente nuevamente.';
                clearPin();
            };
            
            xhr.send(JSON.stringify({ pin: currentPin }));
            
        } catch (error) {
            console.error('Error general:', error);
            messageArea.textContent = 'Error de conexión. Intente nuevamente. Asegúrate de que el servidor backend esté en ejecución.';
            clearPin();
        }
    }
    
    function reset() {
        currentPin = '';
        updatePinDisplay();
        resultContainer.classList.remove('show');
        messageArea.textContent = '';
    }
}); 