# SmartBin - IoT Smart Waste Management System

An IoT-based smart waste bin monitoring system that tracks bin fill levels in real-time and provides intelligent waste management solutions.

## Features

- **Real-time Monitoring**: Track bin fill levels using ultrasonic sensors
- **Cloud Integration**: Store and analyze data in the cloud
- **Web Dashboard**: Monitor multiple bins from a central dashboard
- **Smart Alerts**: Get notified when bins need to be emptied
- **Data Analytics**: Analyze waste patterns and optimize collection routes

## Hardware Requirements

- ESP8266 NodeMCU or ESP32 Development Board
- HC-SR04 Ultrasonic Sensor
- Jumper Wires
- USB Cable for programming
- Power Supply (5V)

## Circuit Connections

### HC-SR04 Ultrasonic Sensor to ESP8266
- VCC → 3.3V or 5V
- GND → GND
- TRIG → D1 (GPIO5)
- ECHO → D2 (GPIO4)

## Software Requirements

- Arduino IDE (for firmware)
- Python 3.7+ (for backend server)
- Node.js (optional, for web dashboard)

## Project Structure

```
SmartBin/
├── firmware/           # ESP8266/Arduino code
│   └── smartbin.ino   # Main firmware file
├── backend/           # Python backend server
│   ├── server.py      # Flask server
│   ├── database.py    # Database operations
│   └── requirements.txt
├── web/               # Web dashboard
│   ├── index.html
│   ├── style.css
│   └── script.js
├── docs/              # Documentation
│   └── circuit_diagram.md
└── config/            # Configuration files
    └── config.example.json
```

## Setup Instructions

### 1. Firmware Setup

1. Install Arduino IDE
2. Add ESP8266 board support:
   - Go to File → Preferences
   - Add to Additional Board Manager URLs: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
3. Install ESP8266 board from Tools → Board → Boards Manager
4. Open `firmware/smartbin.ino`
5. Update WiFi credentials in the code
6. Select your board (NodeMCU 1.0 ESP-12E Module)
7. Upload to your ESP8266

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python server.py
```

### 3. Web Dashboard

Open `web/index.html` in a web browser or serve it using a local server:

```bash
cd web
python -m http.server 8080
```

## Configuration

Copy `config/config.example.json` to `config/config.json` and update with your settings:

```json
{
  "wifi_ssid": "YOUR_WIFI_SSID",
  "wifi_password": "YOUR_WIFI_PASSWORD",
  "server_url": "http://your-server-url:5000",
  "bin_height": 100,
  "update_interval": 60
}
```

## API Endpoints

- `POST /api/data` - Submit bin data
- `GET /api/bins` - Get all bins status
- `GET /api/bins/:id` - Get specific bin data
- `GET /api/stats` - Get statistics

## Usage

1. Power on the SmartBin device
2. The device will connect to WiFi and start monitoring
3. View real-time data on the web dashboard
4. Receive alerts when bins are nearly full

## How It Works

1. **Sensor Reading**: The ultrasonic sensor measures the distance to the waste surface
2. **Fill Level Calculation**: Calculate fill percentage based on bin height
3. **Data Transmission**: Send data to backend server via HTTP/MQTT
4. **Data Storage**: Store readings in database with timestamps
5. **Visualization**: Display data on web dashboard with charts and alerts

## Future Enhancements

- MQTT protocol support for better scalability
- Mobile app for Android/iOS
- Machine learning for waste prediction
- Multi-bin route optimization
- Integration with municipal waste management systems

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

MIT License - feel free to use this project for educational and commercial purposes.

## Contact

For questions or support, please open an issue on GitHub.