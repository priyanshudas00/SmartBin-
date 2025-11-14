// SmartBin Dashboard JavaScript
let serverUrl = localStorage.getItem('serverUrl') || 'http://localhost:5000';
let refreshInterval;

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('serverUrl').value = serverUrl;
    loadData();
    
    // Auto-refresh every 30 seconds
    refreshInterval = setInterval(loadData, 30000);
});

// Update server URL
function updateServerUrl() {
    const newUrl = document.getElementById('serverUrl').value.trim();
    
    if (!newUrl) {
        showMessage('Please enter a valid server URL', 'error');
        return;
    }
    
    serverUrl = newUrl;
    localStorage.setItem('serverUrl', serverUrl);
    showMessage('Server URL updated successfully', 'success');
    loadData();
}

// Refresh data manually
function refreshData() {
    loadData();
    showMessage('Data refreshed', 'success');
}

// Load all data
async function loadData() {
    try {
        await Promise.all([
            loadStatistics(),
            loadBins()
        ]);
    } catch (error) {
        console.error('Error loading data:', error);
        showMessage('Error loading data. Check server connection.', 'error');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${serverUrl}/api/stats`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch statistics');
        }
        
        const data = await response.json();
        const stats = data.statistics;
        
        document.getElementById('totalBins').textContent = stats.total_bins;
        document.getElementById('avgFillLevel').textContent = `${stats.average_fill_level}%`;
        document.getElementById('binsNeedingAttention').textContent = stats.bins_needing_attention;
        document.getElementById('totalReadings').textContent = stats.total_readings;
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load bins data
async function loadBins() {
    try {
        const response = await fetch(`${serverUrl}/api/bins`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch bins data');
        }
        
        const data = await response.json();
        const bins = data.bins;
        
        const binsGrid = document.getElementById('binsGrid');
        
        if (bins.length === 0) {
            binsGrid.innerHTML = '<div class="loading">No bins found. Waiting for data...</div>';
            return;
        }
        
        binsGrid.innerHTML = '';
        
        bins.forEach(bin => {
            const binCard = createBinCard(bin);
            binsGrid.appendChild(binCard);
        });
        
    } catch (error) {
        console.error('Error loading bins:', error);
        const binsGrid = document.getElementById('binsGrid');
        binsGrid.innerHTML = '<div class="loading">Error loading bins. Check server connection.</div>';
    }
}

// Create bin card element
function createBinCard(bin) {
    const card = document.createElement('div');
    const fillLevel = parseFloat(bin.fill_level);
    
    // Determine status class
    let statusClass = 'low';
    let statusText = 'OK';
    
    if (fillLevel >= 80) {
        statusClass = 'full';
        statusText = 'FULL';
    } else if (fillLevel >= 50) {
        statusClass = 'medium';
        statusText = 'MEDIUM';
    }
    
    card.className = `bin-card ${statusClass}`;
    
    // Format timestamp
    const timestamp = new Date(bin.timestamp || bin.created_at).toLocaleString();
    
    card.innerHTML = `
        <div class="bin-header">
            <div class="bin-id">${bin.device_id}</div>
            <div class="bin-status ${statusClass}">${statusText}</div>
        </div>
        <div class="fill-bar-container">
            <div class="fill-bar" style="width: ${fillLevel}%">
                ${fillLevel.toFixed(1)}%
            </div>
        </div>
        <div class="bin-details">
            <p><strong>Distance:</strong> ${parseFloat(bin.distance).toFixed(2)} cm</p>
            <p><strong>Last Update:</strong> ${timestamp}</p>
        </div>
    `;
    
    return card;
}

// Show status message
function showMessage(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type} show`;
    
    setTimeout(() => {
        statusMessage.classList.remove('show');
    }, 3000);
}

// Fetch and display bin history (for future enhancement)
async function loadBinHistory(deviceId) {
    try {
        const response = await fetch(`${serverUrl}/api/bins/${deviceId}?limit=20`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch bin history');
        }
        
        const data = await response.json();
        return data.data;
        
    } catch (error) {
        console.error('Error loading bin history:', error);
        return [];
    }
}

// Test server connection
async function testConnection() {
    try {
        const response = await fetch(`${serverUrl}/`);
        
        if (response.ok) {
            showMessage('Server connection successful', 'success');
            return true;
        } else {
            showMessage('Server connection failed', 'error');
            return false;
        }
    } catch (error) {
        showMessage('Cannot connect to server', 'error');
        return false;
    }
}
