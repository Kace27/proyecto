document.addEventListener('DOMContentLoaded', function() {
    // Configuración
    const SOCKET_URL = 'http://localhost:5002';
    const API_URL = 'http://localhost:5002';
    
    // Elementos DOM
    const ticketsContainer = document.getElementById('tickets-container');
    const connectionStatus = document.createElement('div');
    connectionStatus.id = 'connection-status';
    connectionStatus.className = 'status-disconnected';
    connectionStatus.textContent = 'Desconectado';
    document.body.appendChild(connectionStatus);
    
    // Crear y añadir la nota informativa
    const infoMessage = document.createElement('div');
    infoMessage.className = 'info-message';
    infoMessage.innerHTML = '<strong>Nota:</strong> Haz clic en la cabecera de un ticket para marcarlo como "Listo" y quitarlo de la pantalla.';
    document.querySelector('header').appendChild(infoMessage);
    
    // Estado
    const tickets = {};
    const ticketTimes = {};
    
    // Conectar al socket con opciones
    const socket = io(SOCKET_URL, {
        reconnectionAttempts: 10,
        reconnectionDelay: 1000,
        timeout: 5000,
        transports: ['websocket', 'polling']
    });
    
    // Eventos de socket
    socket.on('connect', function() {
        console.log('Conectado al servidor de websockets');
        connectionStatus.className = 'status-connected';
        connectionStatus.textContent = 'Conectado';
        
        // Obtener tickets activos al conectarse
        fetchActiveTickets();
    });
    
    socket.on('disconnect', function() {
        console.log('Desconectado del servidor de websockets');
        connectionStatus.className = 'status-disconnected';
        connectionStatus.textContent = 'Desconectado';
    });
    
    socket.on('connect_error', function(error) {
        console.error('Error de conexión:', error);
        connectionStatus.className = 'status-error';
        connectionStatus.textContent = 'Error de conexión';
    });
    
    socket.on('new_ticket', function(ticket) {
        console.log('Nuevo ticket recibido:', ticket);
        addOrUpdateTicket(ticket);
    });
    
    socket.on('ticket_status_changed', function(data) {
        console.log('Estado de ticket actualizado:', data);
        if (tickets[data.table]) {
            tickets[data.table].status = data.status;
            updateTicketDisplay(data.table);
        }
    });
    
    // Funciones
    
    // Obtener tickets activos del servidor
    function fetchActiveTickets() {
        fetch(`${API_URL}/tickets/kitchen`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            },
            mode: 'cors'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Tickets activos para cocina:', data);
                
                // Para cada ticket activo, agregarlo a la pantalla
                if (data.tickets) {
                    Object.entries(data.tickets).forEach(([tableNumber, ticket]) => {
                        addOrUpdateTicket(ticket);
                    });
                }
            })
            .catch(error => {
                console.error('Error al obtener tickets para cocina:', error);
                connectionStatus.className = 'status-error';
                connectionStatus.textContent = 'Error al obtener tickets';
            });
    }
    
    // Añadir o actualizar un ticket en la pantalla
    function addOrUpdateTicket(ticket) {
        const tableNumber = ticket.table;
        tickets[tableNumber] = ticket;
        
        // Registrar el tiempo si es nuevo
        if (!ticketTimes[tableNumber]) {
            ticketTimes[tableNumber] = new Date();
        }
        
        updateTicketDisplay(tableNumber);
    }
    
    // Determinar clase de tiempo basado en minutos transcurridos
    function getTimeClass(elapsedMinutes) {
        if (elapsedMinutes <= 2) {
            return 'time-good'; // Verde: 0:00 a 2:00
        } else if (elapsedMinutes <= 3) {
            return 'time-warning'; // Amarillo: 2:01 a 3:00
        } else {
            return 'time-danger'; // Rojo: 3:01 en adelante
        }
    }
    
    // Actualizar la visualización de un ticket
    function updateTicketDisplay(tableNumber) {
        const ticket = tickets[tableNumber];
        if (!ticket) return;
        
        let ticketElement = document.getElementById(`ticket-${tableNumber}`);
        const isNew = !ticketElement;
        
        if (isNew) {
            ticketElement = document.createElement('div');
            ticketElement.className = 'ticket-card';
            ticketElement.id = `ticket-${tableNumber}`;
            ticketsContainer.appendChild(ticketElement);
        }
        
        // Determinar el estado del ticket para el color del encabezado
        const statusClass = ticket.status || 'pending';
        
        // Calcular tiempo transcurrido
        const startTime = ticketTimes[tableNumber];
        const now = new Date();
        const elapsedMinutes = Math.floor((now - startTime) / 60000);
        const elapsedSeconds = Math.floor(((now - startTime) % 60000) / 1000);
        const timeDisplay = `${elapsedMinutes.toString().padStart(2, '0')}:${elapsedSeconds.toString().padStart(2, '0')}`;
        
        // Determinar clase de tiempo en base a minutos transcurridos
        const timeClass = getTimeClass(elapsedMinutes);
        
        // Generar HTML para los elementos del ticket
        const itemsHtml = ticket.items.map(item => `
            <div class="item">
                <div class="item-name">${item.name || 'Artículo sin nombre'}</div>
                ${item.excludedIngredients ? `<div class="item-excluded">Sin: ${item.excludedIngredients.join(', ')}</div>` : ''}
            </div>
        `).join('');
        
        // Actualizar el contenido del ticket
        ticketElement.innerHTML = `
            <div class="ticket-header ${timeClass}" onclick="changeTicketStatus('${tableNumber}', 'ready')">
                <div class="table-info">
                    Mesa ${tableNumber}
                    <span>${ticket.ticket_number || 'Sin número'}</span>
                </div>
                <div class="time-elapsed">${timeDisplay}</div>
            </div>
            <div class="items-container">
                ${itemsHtml}
            </div>
        `;
    }
    
    // Actualizar los tiempos cada segundo
    setInterval(function() {
        Object.keys(tickets).forEach(tableNumber => {
            updateTicketDisplay(tableNumber);
        });
    }, 1000);
    
    // Funciones globales para manejar eventos de botones
    window.changeTicketStatus = function(tableNumber, status) {
        fetch(`${API_URL}/ticket/${tableNumber}/status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`Estado de ticket ${tableNumber} actualizado a ${status}`);
                
                // Si el estado es "ready", remover el ticket de la pantalla
                if (status === 'ready') {
                    const ticketElement = document.getElementById(`ticket-${tableNumber}`);
                    if (ticketElement) {
                        ticketElement.remove();
                    }
                    
                    // Eliminar el ticket del estado local
                    delete tickets[tableNumber];
                    delete ticketTimes[tableNumber];
                }
            } else {
                console.error('Error al actualizar estado:', data.message);
            }
        })
        .catch(error => console.error('Error al actualizar estado:', error));
    };
}); 