# SmartBin Setup Guide

## Quick Start Guide

This guide will help you set up your SmartBin IoT system from scratch.

## Prerequisites

### Hardware
- [ ] ESP8266 NodeMCU or ESP32 board
- [ ] HC-SR04 Ultrasonic Sensor
- [ ] Jumper wires
- [ ] USB cable
- [ ] Computer with USB port

### Software
- [ ] Arduino IDE (Download from https://www.arduino.cc/en/software)
- [ ] Python 3.7 or higher (Download from https://www.python.org/downloads/)
- [ ] Web browser (Chrome, Firefox, Safari, or Edge)

## Step-by-Step Setup

### Part 1: Hardware Assembly (15 minutes)

1. **Assemble the Circuit**
   - Follow the circuit diagram in `docs/circuit_diagram.md`
   - Connect HC-SR04 to ESP8266:
     - VCC → 3.3V or 5V
     - GND → GND
     - TRIG → D1 (GPIO5)
     - ECHO → D2 (GPIO4)

2. **Verify Connections**
   - Double-check all connections
   - Ensure no wires are loose
   - Make sure VCC and GND are not reversed

3. **Mount in Bin**
   - Place sensor at the top of your waste bin
   - Sensor should face downward
   - Measure bin height from sensor to bottom

### Part 2: Arduino Firmware Setup (20 minutes)

1. **Install Arduino IDE**
   ```
   Download from: https://www.arduino.cc/en/software
   Install for your operating system
   ```

2. **Add ESP8266 Board Support**
   - Open Arduino IDE
   - Go to File → Preferences
   - In "Additional Board Manager URLs", add:
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Click OK
   - Go to Tools → Board → Boards Manager
   - Search for "ESP8266"
   - Install "ESP8266 by ESP8266 Community"

3. **Configure Firmware**
   - Open `firmware/smartbin.ino` in Arduino IDE
   - Update these values in the code:
     ```cpp
     const char* ssid = "YOUR_WIFI_SSID";          // Your WiFi name
     const char* password = "YOUR_WIFI_PASSWORD";   // Your WiFi password
     const char* serverUrl = "http://YOUR_SERVER_IP:5000/api/data";
     const int BIN_HEIGHT = 100;                    // Bin height in cm
     const char* deviceId = "BIN001";               // Unique ID for this bin
     ```

4. **Upload Firmware**
   - Connect ESP8266 to computer via USB
   - Select Tools → Board → NodeMCU 1.0 (ESP-12E Module)
   - Select Tools → Port → (your COM port)
   - Click Upload button (→)
   - Wait for "Done uploading" message

5. **Test Firmware**
   - Open Tools → Serial Monitor
   - Set baud rate to 115200
   - You should see WiFi connection messages and sensor readings

### Part 3: Backend Server Setup (10 minutes)

1. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install flask flask-cors
   ```

2. **Run the Server**
   ```bash
   cd backend
   python server.py
   ```

   You should see:
   ```
   Starting SmartBin Server...
   API will be available at http://0.0.0.0:5000
   * Running on http://0.0.0.0:5000
   ```

3. **Test the Server**
   Open a web browser and visit:
   ```
   http://localhost:5000
   ```
   
   You should see the API information.

### Part 4: Web Dashboard Setup (5 minutes)

1. **Open Dashboard**
   - Navigate to the `web` folder
   - Open `index.html` in your web browser
   
   Or use Python's built-in server:
   ```bash
   cd web
   python -m http.server 8080
   ```
   
   Then visit: `http://localhost:8080`

2. **Configure Server URL**
   - In the dashboard, update the Server URL field
   - Enter: `http://localhost:5000` (or your server's IP)
   - Click "Update"

3. **View Data**
   - Wait for the ESP8266 to send data (every 60 seconds by default)
   - Dashboard will auto-refresh every 30 seconds
   - Click "Refresh Data" to manually update

## Testing Your Setup

### Test 1: Hardware Connection
1. Open Serial Monitor in Arduino IDE
2. You should see distance measurements
3. Place your hand above the sensor
4. Distance should change accordingly

### Test 2: Backend API
1. Test the API endpoint:
   ```bash
   curl http://localhost:5000/api/bins
   ```
2. You should see JSON response with bin data

### Test 3: End-to-End
1. Ensure firmware is running on ESP8266
2. Ensure backend server is running
3. Open web dashboard
4. You should see your bin with real-time data

## Common Issues and Solutions

### Issue: ESP8266 Won't Connect to WiFi
**Solution:**
- Check WiFi credentials in firmware
- Ensure WiFi is 2.4GHz (ESP8266 doesn't support 5GHz)
- Check if WiFi network is reachable
- Restart ESP8266

### Issue: Sensor Readings are Incorrect
**Solution:**
- Check all connections
- Ensure sensor is mounted properly
- Verify BIN_HEIGHT value in firmware
- Make sure sensor is not too close to bin walls

### Issue: Data Not Showing in Dashboard
**Solution:**
- Check if backend server is running
- Verify server URL in dashboard settings
- Check browser console for errors (F12)
- Ensure ESP8266 can reach the server
- Check server firewall settings

### Issue: Backend Server Won't Start
**Solution:**
- Ensure Python is installed correctly
- Install missing dependencies: `pip install -r requirements.txt`
- Check if port 5000 is already in use
- Try a different port in server.py

## Network Configuration

### Same Computer Setup
- ESP8266, Backend, and Dashboard on same network
- Use `localhost` or `127.0.0.1` for server URL

### Local Network Setup
- Backend runs on a server/computer
- Find server's local IP: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
- Use `http://192.168.X.X:5000` as server URL
- Ensure all devices are on same network

### Internet/Cloud Setup
- Deploy backend to cloud service (AWS, Heroku, DigitalOcean)
- Use public URL in firmware and dashboard
- Consider security (HTTPS, authentication)

## Configuration Tips

### Multiple Bins
1. Clone firmware for each bin
2. Change `deviceId` to unique value (BIN001, BIN002, etc.)
3. Upload to each ESP8266
4. All bins will appear in dashboard automatically

### Adjust Update Interval
In firmware, change:
```cpp
const int UPDATE_INTERVAL = 60000;  // 60 seconds
```

### Adjust Alert Threshold
In `backend/database.py`, line 140:
```python
WHERE fill_level > 80  # Change 80 to your threshold
```

## Production Deployment

For production use:
1. Use HTTPS for backend server
2. Implement authentication
3. Use proper database (PostgreSQL/MySQL instead of SQLite)
4. Set up monitoring and logging
5. Configure automatic backups
6. Use environment variables for sensitive data

## Next Steps

- [ ] Add more bins to your system
- [ ] Set up email/SMS alerts
- [ ] Implement MQTT for better scalability
- [ ] Add data analytics and predictions
- [ ] Create mobile app
- [ ] Integrate with municipal waste management

## Support

For issues or questions:
- Check the documentation in `docs/` folder
- Review the code comments
- Open an issue on GitHub
- Contact the maintainers

## Maintenance

Regular maintenance tasks:
- Clean sensor lens periodically
- Check WiFi connection stability
- Monitor server logs
- Backup database regularly
- Update firmware as needed
- Check battery/power supply

Congratulations! Your SmartBin system is now set up and running! 🎉
