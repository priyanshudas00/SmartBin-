"""
SmartBin Backend Server
Flask-based REST API for receiving and serving bin data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import database as db

app = Flask(__name__)
CORS(app)  # Enable CORS for web dashboard

# Initialize database
db.init_database()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "SmartBin API Server",
        "version": "1.0",
        "endpoints": {
            "POST /api/data": "Submit bin data",
            "GET /api/bins": "Get all bins status",
            "GET /api/bins/<device_id>": "Get specific bin data",
            "GET /api/stats": "Get statistics"
        }
    })

@app.route('/api/data', methods=['POST'])
def receive_data():
    """Receive data from SmartBin devices"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['device_id', 'distance', 'fill_level']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Add timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        # Store data in database
        db.insert_bin_data(
            device_id=data['device_id'],
            distance=data['distance'],
            fill_level=data['fill_level'],
            timestamp=data.get('timestamp')
        )
        
        return jsonify({
            "status": "success",
            "message": "Data received successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bins', methods=['GET'])
def get_all_bins():
    """Get status of all bins"""
    try:
        bins = db.get_all_bins_latest()
        return jsonify({
            "status": "success",
            "count": len(bins),
            "bins": bins
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bins/<device_id>', methods=['GET'])
def get_bin_data(device_id):
    """Get historical data for a specific bin"""
    try:
        limit = request.args.get('limit', 100, type=int)
        data = db.get_bin_history(device_id, limit)
        
        if not data:
            return jsonify({
                "status": "success",
                "message": "No data found for this device",
                "device_id": device_id,
                "data": []
            }), 200
        
        return jsonify({
            "status": "success",
            "device_id": device_id,
            "count": len(data),
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    try:
        stats = db.get_statistics()
        return jsonify({
            "status": "success",
            "statistics": stats
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bins/<device_id>/latest', methods=['GET'])
def get_bin_latest(device_id):
    """Get latest reading for a specific bin"""
    try:
        data = db.get_bin_latest(device_id)
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data found for this device"
            }), 404
        
        return jsonify({
            "status": "success",
            "device_id": device_id,
            "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting SmartBin Server...")
    print("API will be available at http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
