"""
Database operations for SmartBin
Uses SQLite for data storage
"""

import sqlite3
from datetime import datetime
import os

DATABASE_PATH = 'smartbin.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create bin_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bin_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            distance REAL NOT NULL,
            fill_level REAL NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_device_timestamp 
        ON bin_data(device_id, timestamp DESC)
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def insert_bin_data(device_id, distance, fill_level, timestamp=None):
    """Insert bin data into database"""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO bin_data (device_id, distance, fill_level, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (device_id, distance, fill_level, timestamp))
    
    conn.commit()
    conn.close()

def get_all_bins_latest():
    """Get latest reading for all bins"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT device_id, distance, fill_level, timestamp, created_at
        FROM bin_data
        WHERE id IN (
            SELECT MAX(id)
            FROM bin_data
            GROUP BY device_id
        )
        ORDER BY device_id
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    bins = []
    for row in rows:
        bins.append({
            'device_id': row['device_id'],
            'distance': row['distance'],
            'fill_level': row['fill_level'],
            'timestamp': row['timestamp'],
            'created_at': row['created_at']
        })
    
    return bins

def get_bin_history(device_id, limit=100):
    """Get historical data for a specific bin"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, device_id, distance, fill_level, timestamp, created_at
        FROM bin_data
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
    ''', (device_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row['id'],
            'device_id': row['device_id'],
            'distance': row['distance'],
            'fill_level': row['fill_level'],
            'timestamp': row['timestamp'],
            'created_at': row['created_at']
        })
    
    return history

def get_bin_latest(device_id):
    """Get latest reading for a specific bin"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT device_id, distance, fill_level, timestamp, created_at
        FROM bin_data
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (device_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'device_id': row['device_id'],
            'distance': row['distance'],
            'fill_level': row['fill_level'],
            'timestamp': row['timestamp'],
            'created_at': row['created_at']
        }
    return None

def get_statistics():
    """Get overall statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total bins
    cursor.execute('SELECT COUNT(DISTINCT device_id) as total_bins FROM bin_data')
    total_bins = cursor.fetchone()['total_bins']
    
    # Total readings
    cursor.execute('SELECT COUNT(*) as total_readings FROM bin_data')
    total_readings = cursor.fetchone()['total_readings']
    
    # Average fill level
    cursor.execute('''
        SELECT AVG(fill_level) as avg_fill_level
        FROM bin_data
        WHERE id IN (
            SELECT MAX(id)
            FROM bin_data
            GROUP BY device_id
        )
    ''')
    avg_fill_level = cursor.fetchone()['avg_fill_level']
    
    # Bins needing attention (>80% full)
    cursor.execute('''
        SELECT COUNT(*) as bins_needing_attention
        FROM bin_data
        WHERE fill_level > 80
        AND id IN (
            SELECT MAX(id)
            FROM bin_data
            GROUP BY device_id
        )
    ''')
    bins_needing_attention = cursor.fetchone()['bins_needing_attention']
    
    conn.close()
    
    return {
        'total_bins': total_bins,
        'total_readings': total_readings,
        'average_fill_level': round(avg_fill_level, 2) if avg_fill_level else 0,
        'bins_needing_attention': bins_needing_attention
    }
