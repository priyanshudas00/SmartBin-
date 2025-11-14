# Circuit Diagram

## SmartBin Hardware Setup

### Components Required
1. ESP8266 NodeMCU Development Board
2. HC-SR04 Ultrasonic Sensor
3. Breadboard (optional)
4. Jumper Wires (Male-to-Female)
5. USB Cable (Micro USB)
6. 5V Power Supply

### Pin Connections

#### ESP8266 NodeMCU to HC-SR04 Ultrasonic Sensor

```
HC-SR04          ESP8266 NodeMCU
--------         ----------------
VCC      ------>  3.3V or 5V (VIN)
GND      ------>  GND
TRIG     ------>  D1 (GPIO5)
ECHO     ------>  D2 (GPIO4)
```

### Circuit Diagram (ASCII Art)

```
                    ESP8266 NodeMCU
                   +----------------+
                   |                |
                   |             3V3|----+
                   |                |    |
                   |             GND|--+ |
                   |                |  | |
                   |          D1(G5)|--|-|-+
                   |                |  | | |
                   |          D2(G4)|--|-|-|-+
                   |                |  | | | |
                   |            USB |  | | | |
                   +-------||-------+  | | | |
                           ||          | | | |
                      (To Computer)    | | | |
                                       | | | |
                    HC-SR04 Sensor     | | | |
                   +----------------+  | | | |
                   |                |  | | | |
                   |  [   ] [   ]   |  | | | |
              VCC--|  Trig   Echo   |  | | | |
                   |                |  | | | |
              GND--|                |  | | | |
                   +----------------+  | | | |
                        |   |   |   |  | | | |
                        |   |   |   +--+ | | |
                        |   |   +--------+ | |
                        |   +--------------+ |
                        +--------------------+
```

### Detailed Connection Instructions

1. **Power Connections:**
   - Connect VCC of HC-SR04 to 3.3V or 5V pin of ESP8266
   - Connect GND of HC-SR04 to GND pin of ESP8266

2. **Signal Connections:**
   - Connect TRIG pin of HC-SR04 to D1 (GPIO5) of ESP8266
   - Connect ECHO pin of HC-SR04 to D2 (GPIO4) of ESP8266

3. **Power Supply:**
   - You can power the ESP8266 via USB from a computer or power adapter
   - For permanent installation, use a 5V power adapter with micro USB connector

### Important Notes

- **Voltage Levels:** The HC-SR04 operates at 5V, but ESP8266 GPIO pins are 3.3V. However, the echo pin output is 5V which could potentially damage ESP8266. For safer operation, consider using a voltage divider (2 resistors: 1kΩ and 2kΩ) on the ECHO pin.

- **Voltage Divider for ECHO pin (Recommended):**
  ```
  ECHO (5V) ----[1kΩ]----+----[2kΩ]---- GND
                          |
                      D2 (GPIO4)
  ```

- **Sensor Placement:** 
  - Mount the ultrasonic sensor at the top of the bin, facing downward
  - Ensure the sensor is centered and level
  - Keep the sensor away from the bin walls to avoid false readings

### Mounting the Sensor

1. **Position:** Mount the HC-SR04 at the top center of the bin lid
2. **Orientation:** The sensor should face directly downward into the bin
3. **Height:** Measure the total height from sensor to bin bottom (BIN_HEIGHT in code)
4. **Protection:** Consider using a protective case to shield from moisture

### Testing the Circuit

1. Connect all components as per the diagram
2. Upload the firmware to ESP8266
3. Open Serial Monitor (115200 baud rate)
4. You should see distance readings
5. Test by placing objects at different heights in the bin

### Troubleshooting

- **No readings:** Check all connections, especially GND
- **Incorrect readings:** Ensure sensor is level and centered
- **Inconsistent readings:** Check for loose connections or interference
- **ESP8266 won't boot:** Disconnect ECHO pin during boot, reconnect after boot

### Multiple Bin Setup

To monitor multiple bins, replicate the circuit for each bin:
- Use a unique device_id in the firmware for each bin
- Each bin needs its own ESP8266 and ultrasonic sensor
- All bins connect to the same WiFi and backend server

### Power Options

1. **USB Power:** Simple, good for development and indoor use
2. **Wall Adapter:** Reliable for permanent installations
3. **Battery Pack:** For portable or outdoor installations (requires power management)
4. **Solar Panel:** For outdoor installations with rechargeable battery backup
