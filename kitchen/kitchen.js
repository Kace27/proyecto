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
        
        // Generar HTML para los elementos del ticket
        const itemsHtml = ticket.items.map(item => `
            <div class="item">
                <div class="item-tag">#${item.customizations ? 'Personalizado' : 'Estándar'}</div>
                <div class="item-name">${item.name || 'Artículo sin nombre'}</div>
                <div class="item-id">ID: ${item.id || 'N/A'}</div>
                <div class="item-price">$${item.price || 0} × ${item.quantity || 1}</div>
                ${item.excludedIngredients ? `<div class="item-excluded">Sin: ${item.excludedIngredients.join(', ')}</div>` : ''}
                <button class="btn-done" onclick="markItemDone(this)">Done</button>
            </div>
        `).join('');
        
        // Actualizar el contenido del ticket
        ticketElement.innerHTML = `
            <div class="ticket-header ${statusClass}">
                <div class="table-info">
                    Mesa ${tableNumber}
                    <span>${ticket.ticket_number || 'Sin número'}</span>
                </div>
                <div class="time-elapsed">${timeDisplay}</div>
            </div>
            <div class="items-container">
                ${itemsHtml}
            </div>
            <div class="controls">
                <button class="btn-action" onclick="changeTicketStatus('${tableNumber}', 'preparing')">Preparando</button>
                <button class="btn-action" onclick="changeTicketStatus('${tableNumber}', 'ready')" style="background: #34C759">Listo</button>
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
    window.markItemDone = function(button) {
        button.textContent = '✓';
        button.disabled = true;
        button.style.backgroundColor = '#34C759';
    };
    
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
            } else {
                console.error('Error al actualizar estado:', data.message);
            }
        })
        .catch(error => console.error('Error al actualizar estado:', error));
    };
}); 