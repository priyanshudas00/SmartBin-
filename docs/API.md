# SmartBin API Documentation

## Overview
The SmartBin API provides endpoints for receiving data from IoT devices and serving data to the web dashboard.

## Base URL
```
http://your-server-ip:5000
```

## Endpoints

### 1. Home Endpoint
Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "SmartBin API Server",
  "version": "1.0",
  "endpoints": {
    "POST /api/data": "Submit bin data",
    "GET /api/bins": "Get all bins status",
    "GET /api/bins/<device_id>": "Get specific bin data",
    "GET /api/stats": "Get statistics"
  }
}
```

---

### 2. Submit Bin Data
Receive data from SmartBin IoT devices.

**Endpoint:** `POST /api/data`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "device_id": "BIN001",
  "distance": 25.5,
  "fill_level": 74.5,
  "timestamp": "2024-01-15T10:30:00"
}
```

**Parameters:**
- `device_id` (string, required): Unique identifier for the bin
- `distance` (float, required): Distance measured by sensor in cm
- `fill_level` (float, required): Calculated fill percentage (0-100)
- `timestamp` (string, optional): ISO 8601 timestamp. Auto-generated if not provided.

**Success Response:**
```json
{
  "status": "success",
  "message": "Data received successfully"
}
```

**Error Response:**
```json
{
  "error": "Missing required field: device_id"
}
```

**Status Codes:**
- `201`: Data received successfully
- `400`: Bad request (missing fields)
- `500`: Internal server error

---

### 3. Get All Bins Status
Retrieve the latest status of all bins.

**Endpoint:** `GET /api/bins`

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "bins": [
    {
      "device_id": "BIN001",
      "distance": 25.5,
      "fill_level": 74.5,
      "timestamp": "2024-01-15T10:30:00",
      "created_at": "2024-01-15 10:30:00"
    },
    {
      "device_id": "BIN002",
      "distance": 60.0,
      "fill_level": 40.0,
      "timestamp": "2024-01-15T10:29:55",
      "created_at": "2024-01-15 10:29:55"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error

---

### 4. Get Bin History
Retrieve historical data for a specific bin.

**Endpoint:** `GET /api/bins/<device_id>`

**Query Parameters:**
- `limit` (integer, optional): Maximum number of records to return. Default: 100

**Example:**
```
GET /api/bins/BIN001?limit=50
```

**Response:**
```json
{
  "status": "success",
  "device_id": "BIN001",
  "count": 50,
  "data": [
    {
      "id": 150,
      "device_id": "BIN001",
      "distance": 25.5,
      "fill_level": 74.5,
      "timestamp": "2024-01-15T10:30:00",
      "created_at": "2024-01-15 10:30:00"
    },
    {
      "id": 149,
      "device_id": "BIN001",
      "distance": 26.0,
      "fill_level": 74.0,
      "timestamp": "2024-01-15T10:29:00",
      "created_at": "2024-01-15 10:29:00"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `500`: Internal server error

---

### 5. Get Latest Bin Reading
Get the most recent reading for a specific bin.

**Endpoint:** `GET /api/bins/<device_id>/latest`

**Example:**
```
GET /api/bins/BIN001/latest
```

**Response:**
```json
{
  "status": "success",
  "device_id": "BIN001",
  "data": {
    "device_id": "BIN001",
    "distance": 25.5,
    "fill_level": 74.5,
    "timestamp": "2024-01-15T10:30:00",
    "created_at": "2024-01-15 10:30:00"
  }
}
```

**Status Codes:**
- `200`: Success
- `404`: No data found for device
- `500`: Internal server error

---

### 6. Get Statistics
Retrieve overall system statistics.

**Endpoint:** `GET /api/stats`

**Response:**
```json
{
  "status": "success",
  "statistics": {
    "total_bins": 5,
    "total_readings": 1250,
    "average_fill_level": 62.5,
    "bins_needing_attention": 2
  }
}
```

**Response Fields:**
- `total_bins`: Total number of unique bins in the system
- `total_readings`: Total number of readings received
- `average_fill_level`: Average fill level across all bins
- `bins_needing_attention`: Number of bins with fill level > 80%

**Status Codes:**
- `200`: Success
- `500`: Internal server error

---

## Error Handling

All endpoints return errors in the following format:

```json
{
  "error": "Error message description"
}
```

Common error codes:
- `400`: Bad Request - Invalid input data
- `404`: Not Found - Resource doesn't exist
- `500`: Internal Server Error - Server-side error

---

## CORS

CORS is enabled for all origins to allow web dashboard access.

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing rate limiting based on your requirements.

---

## Authentication

Currently, the API doesn't require authentication. For production deployment, consider implementing:
- API keys
- JWT tokens
- OAuth 2.0

---

## Examples

### Using cURL

**Submit data:**
```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "BIN001",
    "distance": 25.5,
    "fill_level": 74.5
  }'
```

**Get all bins:**
```bash
curl http://localhost:5000/api/bins
```

**Get bin history:**
```bash
curl http://localhost:5000/api/bins/BIN001?limit=20
```

### Using Python

```python
import requests

# Submit data
data = {
    "device_id": "BIN001",
    "distance": 25.5,
    "fill_level": 74.5
}
response = requests.post("http://localhost:5000/api/data", json=data)
print(response.json())

# Get all bins
response = requests.get("http://localhost:5000/api/bins")
bins = response.json()
print(bins)
```

### Using JavaScript

```javascript
// Submit data
fetch('http://localhost:5000/api/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    device_id: 'BIN001',
    distance: 25.5,
    fill_level: 74.5
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Get all bins
fetch('http://localhost:5000/api/bins')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## Testing

You can test the API using tools like:
- Postman
- cURL
- Python requests library
- JavaScript fetch API

For local development, the server runs on `http://localhost:5000`
