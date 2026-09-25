from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

lock = threading.Lock()

driver_data = {
    "drowsiness": False,
    "distraction": False,
    "yawning": False,
    "timestamp": 0
}

road_data = {
    "vehicles": 0,
    "people": 0,
    "motorcycles": 0,
    "trucks": 0,
    "hazard": False,
    "timestamp": 0
}


def calculate_risk(driver, road):
    score = 0
    reasons = []

    if driver.get("drowsiness"):
        score += 45
        reasons.append("Drowsiness detected")

    if driver.get("distraction"):
        score += 30
        reasons.append("Driver distraction detected")

    if driver.get("yawning"):
        score += 15
        reasons.append("Yawning detected")

    if road.get("hazard"):
        score += 35
        reasons.append("Road hazard detected")

    # Prototype road-density contribution.
    if road.get("vehicles", 0) >= 5:
        score += 10
        reasons.append("High vehicle density")

    score = min(score, 100)

    if score >= 70:
        level = "CRITICAL"
        braking = True
        hazard_lights = True
    elif score >= 35:
        level = "WARNING"
        braking = False
        hazard_lights = True
    else:
        level = "SAFE"
        braking = False
        hazard_lights = False

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons,
        "controlled_braking": braking,
        "hazard_lights": hazard_lights
    }


@app.get("/")
def home():
    return jsonify({
        "service": "Intelligent Heavy Vehicle Safety Engine",
        "status": "running"
    })


@app.post("/driver")
def update_driver():
    global driver_data

    incoming = request.get_json(silent=True) or {}

    with lock:
        driver_data.update({
            "drowsiness": bool(incoming.get("drowsiness", False)),
            "distraction": bool(incoming.get("distraction", False)),
            "yawning": bool(incoming.get("yawning", False)),
            "timestamp": time.time()
        })

    return jsonify({"status": "driver data received"})


@app.post("/road")
def update_road():
    global road_data

    incoming = request.get_json(silent=True) or {}

    with lock:
        road_data.update({
            "vehicles": int(incoming.get("vehicles", 0)),
            "people": int(incoming.get("people", 0)),
            "motorcycles": int(incoming.get("motorcycles", 0)),
            "trucks": int(incoming.get("trucks", 0)),
            "hazard": bool(incoming.get("hazard", False)),
            "timestamp": time.time()
        })

    return jsonify({"status": "road data received"})


@app.get("/status")
def status():
    with lock:
        result = calculate_risk(driver_data, road_data)

        return jsonify({
            "driver": driver_data,
            "road": road_data,
            "safety": result
        })


if __name__ == "__main__":
    print("============================================")
    print(" Intelligent Heavy Vehicle Safety Engine")
    print("============================================")
    print("Server running on port 5000")
    print("Use the L3 laptop's local IP address for")
    print("L1/L2/L4 communication.")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
