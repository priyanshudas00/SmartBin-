"""
Test script for SmartBin Backend API
Simulates IoT device sending data and tests all endpoints
"""

import requests
import json
import time
import random
from datetime import datetime

# Configuration
SERVER_URL = "http://localhost:5000"
DEVICE_IDS = ["BIN001", "BIN002", "BIN003"]

def test_connection():
    """Test if server is running"""
    print("Testing server connection...")
    try:
        response = requests.get(f"{SERVER_URL}/")
        if response.status_code == 200:
            print("✓ Server is running")
            print(f"  Response: {response.json()['message']}")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running?")
        return False

def generate_sample_data(device_id, bin_height=100):
    """Generate realistic sample data"""
    # Simulate different fill levels
    distance = random.uniform(10, 90)
    fill_level = ((bin_height - distance) / bin_height) * 100
    
    if fill_level < 0:
        fill_level = 0
    if fill_level > 100:
        fill_level = 100
    
    return {
        "device_id": device_id,
        "distance": round(distance, 2),
        "fill_level": round(fill_level, 2),
        "timestamp": datetime.now().isoformat()
    }

def test_post_data():
    """Test POST /api/data endpoint"""
    print("\nTesting POST /api/data...")
    
    for device_id in DEVICE_IDS:
        data = generate_sample_data(device_id)
        print(f"\n  Sending data for {device_id}:")
        print(f"    Distance: {data['distance']} cm")
        print(f"    Fill Level: {data['fill_level']}%")
        
        try:
            response = requests.post(
                f"{SERVER_URL}/api/data",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                print(f"  ✓ Data submitted successfully for {device_id}")
            else:
                print(f"  ✗ Error: {response.status_code}")
                print(f"    {response.json()}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")
    
    time.sleep(1)  # Wait for data to be processed

def test_get_all_bins():
    """Test GET /api/bins endpoint"""
    print("\nTesting GET /api/bins...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/bins")
        
        if response.status_code == 200:
            data = response.json()
            bins = data.get("bins", [])
            print(f"  ✓ Retrieved {len(bins)} bins")
            
            for bin_data in bins:
                print(f"\n    {bin_data['device_id']}:")
                print(f"      Fill Level: {bin_data['fill_level']}%")
                print(f"      Distance: {bin_data['distance']} cm")
                print(f"      Last Update: {bin_data['timestamp']}")
        else:
            print(f"  ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

def test_get_bin_history(device_id):
    """Test GET /api/bins/<device_id> endpoint"""
    print(f"\nTesting GET /api/bins/{device_id}...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/bins/{device_id}?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            history = data.get("data", [])
            print(f"  ✓ Retrieved {len(history)} records for {device_id}")
            
            if history:
                print(f"    Latest reading:")
                latest = history[0]
                print(f"      Fill Level: {latest['fill_level']}%")
                print(f"      Distance: {latest['distance']} cm")
        else:
            print(f"  ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

def test_get_bin_latest(device_id):
    """Test GET /api/bins/<device_id>/latest endpoint"""
    print(f"\nTesting GET /api/bins/{device_id}/latest...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/bins/{device_id}/latest")
        
        if response.status_code == 200:
            data = response.json()
            bin_data = data.get("data", {})
            print(f"  ✓ Retrieved latest data for {device_id}")
            print(f"    Fill Level: {bin_data['fill_level']}%")
            print(f"    Distance: {bin_data['distance']} cm")
        else:
            print(f"  ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

def test_get_statistics():
    """Test GET /api/stats endpoint"""
    print("\nTesting GET /api/stats...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/stats")
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get("statistics", {})
            print("  ✓ Retrieved statistics:")
            print(f"    Total Bins: {stats['total_bins']}")
            print(f"    Total Readings: {stats['total_readings']}")
            print(f"    Average Fill Level: {stats['average_fill_level']}%")
            print(f"    Bins Needing Attention: {stats['bins_needing_attention']}")
        else:
            print(f"  ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

def simulate_continuous_data(duration=60, interval=5):
    """Simulate continuous data sending"""
    print(f"\nSimulating continuous data for {duration} seconds...")
    print(f"Sending data every {interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    start_time = time.time()
    count = 0
    
    try:
        while time.time() - start_time < duration:
            count += 1
            print(f"\n--- Update #{count} ---")
            
            for device_id in DEVICE_IDS:
                data = generate_sample_data(device_id)
                response = requests.post(
                    f"{SERVER_URL}/api/data",
                    json=data
                )
                
                if response.status_code == 201:
                    print(f"  ✓ {device_id}: {data['fill_level']}%")
                else:
                    print(f"  ✗ {device_id}: Error")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
    
    print(f"\nSent {count * len(DEVICE_IDS)} data points")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("SmartBin Backend API Test Suite")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        print("\n✗ Server is not running. Please start the server first.")
        print("  Run: python backend/server.py")
        return
    
    # Test endpoints
    test_post_data()
    test_get_all_bins()
    test_get_bin_history(DEVICE_IDS[0])
    test_get_bin_latest(DEVICE_IDS[0])
    test_get_statistics()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

def main():
    """Main function"""
    print("SmartBin Backend Test Script\n")
    print("Options:")
    print("1. Run all tests")
    print("2. Simulate continuous data")
    print("3. Send single data point")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_all_tests()
    elif choice == "2":
        duration = input("Duration in seconds (default 60): ").strip()
        duration = int(duration) if duration else 60
        simulate_continuous_data(duration=duration)
    elif choice == "3":
        device_id = input(f"Device ID (default BIN001): ").strip() or "BIN001"
        data = generate_sample_data(device_id)
        print(f"\nSending data: {json.dumps(data, indent=2)}")
        response = requests.post(f"{SERVER_URL}/api/data", json=data)
        print(f"Response: {response.json()}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
