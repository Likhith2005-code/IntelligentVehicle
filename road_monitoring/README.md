# L2 — Road Monitoring

This module is the front/road-camera component of the Intelligent Heavy Vehicle Safety system.

## Features
- Webcam capture
- YOLO object detection
- Detection of person, bicycle, car, motorcycle, bus and truck
- Live bounding boxes and object counts

## Setup (Windows PowerShell)

```powershell
cd road_monitoring
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python road_monitor.py
```

Then run:

```powershell
python road_monitor.py
```

The first run downloads the YOLO model automatically if it is not already available.

Press `Q` to stop.

## Note

This is the initial road-monitoring prototype. It detects road objects but does not yet claim to estimate collision distance or perform autonomous braking. Those features will be added later through the safety-engine integration.
