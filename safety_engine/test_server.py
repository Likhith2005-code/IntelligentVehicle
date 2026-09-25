import requests

BASE_URL = "http://127.0.0.1:5000"

driver = {
    "drowsiness": True,
    "distraction": False,
    "yawning": False
}

road = {
    "vehicles": 2,
    "people": 0,
    "motorcycles": 1,
    "trucks": 1,
    "hazard": True
}

print("Sending driver data...")
print(requests.post(f"{BASE_URL}/driver", json=driver).json())

print("Sending road data...")
print(requests.post(f"{BASE_URL}/road", json=road).json())

print("\nSafety result:")
print(requests.get(f"{BASE_URL}/status").json())
