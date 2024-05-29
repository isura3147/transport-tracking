from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bus_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bus_id TEXT,
                        latitude REAL,
                        longitude REAL,
                        speed REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

@app.route('/api/update_location', methods=['GET'])
def update_location():
    bus_id = request.args.get('bus_id', 'bus1')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    speed = request.args.get('speed')

    conn = sqlite3.connect('bus_tracking.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO locations (bus_id, latitude, longitude, speed) VALUES (?, ?, ?, ?)",
                   (bus_id, lat, lng, speed))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route('/api/get_location', methods=['GET'])
def get_location():
    bus_id = request.args.get('bus_id', 'bus1')
    conn = sqlite3.connect('bus_tracking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude, speed, timestamp FROM locations WHERE bus_id = ? ORDER BY timestamp DESC LIMIT 1", (bus_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            "latitude": row[0],
            "longitude": row[1],
            "speed": row[2],
            "timestamp": row[3]
        })
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
