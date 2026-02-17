from SimConnect import SimConnect, AircraftRequests
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import time
import math # Added for conversion

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve the plane icon from a local folder named 'static'
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def start_sim_loop():
    try:
        sm = SimConnect()
        aq = AircraftRequests(sm)
        print("Connected to FS2024!")
        
        while True:
            # Fix: Convert Radians to Degrees
            raw_heading = aq.get("PLANE_HEADING_DEGREES_TRUE") or 0
            heading_deg = math.degrees(raw_heading)

            data = {
                "lat": aq.get("PLANE_LATITUDE"),
                "lon": aq.get("PLANE_LONGITUDE"),
                "heading": heading_deg,
                "airspeed": aq.get("AIRSPEED_INDICATED"),
                "alt": aq.get("PLANE_ALTITUDE")
            }
            socketio.emit('telemetry', data)
            time.sleep(0.5) 
    except Exception as e:
        print(f"Waiting for Simulator... {e}")

if __name__ == '__main__':
    socketio.start_background_task(start_sim_loop)
    socketio.run(app, port=5000)