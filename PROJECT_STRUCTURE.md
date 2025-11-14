# SmartBin Project - File Structure

This document provides an overview of the SmartBin IoT project structure.

## Project Structure

```
SmartBin/
│
├── README.md                      # Main project documentation
├── .gitignore                     # Git ignore rules
│
├── firmware/                      # ESP8266/Arduino firmware
│   └── smartbin.ino              # Main firmware code for IoT device
│
├── backend/                       # Python Flask backend server
│   ├── server.py                 # Flask REST API server
│   ├── database.py               # SQLite database operations
│   ├── requirements.txt          # Python dependencies
│   └── test_api.py               # API testing script
│
├── web/                          # Web dashboard (HTML/CSS/JS)
│   ├── index.html                # Main dashboard page
│   ├── style.css                 # Dashboard styles
│   └── script.js                 # Dashboard functionality
│
├── config/                       # Configuration files
│   └── config.example.json       # Example configuration
│
└── docs/                         # Documentation
    ├── API.md                    # API documentation
    ├── SETUP.md                  # Setup guide
    └── circuit_diagram.md        # Hardware circuit diagram
```

## File Descriptions

### Root Files
- **README.md**: Complete project documentation with features, setup, and usage instructions
- **.gitignore**: Excludes build artifacts, dependencies, and sensitive files from git

### Firmware (firmware/)
- **smartbin.ino**: Arduino sketch for ESP8266 that reads ultrasonic sensor data and sends it to the backend server via HTTP POST requests

### Backend (backend/)
- **server.py**: Flask REST API server with endpoints for receiving and serving bin data
- **database.py**: Database operations using SQLite for storing bin readings
- **requirements.txt**: Python package dependencies (Flask, Flask-CORS)
- **test_api.py**: Comprehensive testing script to validate API functionality

### Web Dashboard (web/)
- **index.html**: Dashboard interface showing bin status, fill levels, and statistics
- **style.css**: Modern, responsive styling with gradient design
- **script.js**: Client-side logic for fetching data and updating the UI in real-time

### Configuration (config/)
- **config.example.json**: Template configuration file with all required settings

### Documentation (docs/)
- **API.md**: Detailed API documentation with all endpoints, parameters, and examples
- **SETUP.md**: Step-by-step setup guide from hardware assembly to deployment
- **circuit_diagram.md**: Hardware wiring diagram and assembly instructions

## Technology Stack

### Hardware
- ESP8266 NodeMCU (WiFi-enabled microcontroller)
- HC-SR04 Ultrasonic Sensor (distance measurement)

### Firmware
- Arduino IDE / PlatformIO
- ESP8266 WiFi library
- HTTP client for data transmission

### Backend
- Python 3.7+
- Flask (web framework)
- Flask-CORS (cross-origin support)
- SQLite (database)

### Frontend
- HTML5
- CSS3 (responsive design)
- Vanilla JavaScript (no frameworks)
- Fetch API for HTTP requests

## Data Flow

1. **Sensor Reading**: HC-SR04 measures distance to waste surface
2. **Data Processing**: ESP8266 calculates fill percentage
3. **Data Transmission**: HTTP POST to backend API
4. **Data Storage**: Backend stores data in SQLite database
5. **Data Retrieval**: Web dashboard fetches data via REST API
6. **Visualization**: Dashboard displays bin status and statistics

## Key Features

### Firmware
- WiFi connectivity with auto-reconnect
- Ultrasonic sensor integration
- Fill level calculation
- Configurable update intervals
- Serial monitoring for debugging

### Backend
- RESTful API design
- CORS support for web access
- SQLite database with indexing
- Multiple endpoint support
- Error handling

### Web Dashboard
- Real-time data display
- Auto-refresh functionality
- Responsive design
- Color-coded bin status
- Statistics overview
- Configurable server URL

## Getting Started

1. Read `README.md` for project overview
2. Follow `docs/SETUP.md` for step-by-step setup
3. Review `docs/circuit_diagram.md` for hardware assembly
4. Refer to `docs/API.md` for API integration

## Development Workflow

1. **Hardware Setup**: Assemble circuit as per circuit_diagram.md
2. **Firmware Upload**: Configure and upload firmware/smartbin.ino
3. **Backend Start**: Run backend/server.py
4. **Dashboard Open**: Open web/index.html in browser
5. **Testing**: Use backend/test_api.py to verify functionality

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See README.md for details
