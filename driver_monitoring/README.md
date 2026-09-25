# L1 — Driver Monitoring

This module is the driver-monitoring prototype for the Intelligent Heavy Vehicle Safety system.

## Features
- Webcam capture
- Face landmarks
- Eye-closure based drowsiness detection
- Simple head/distraction detection
- Live driver status

## Setup (Windows PowerShell)

```powershell
cd driver_monitoring
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python driver_monitor.py
```

Press `Q` to stop.

Note: This is a hackathon prototype. Detection thresholds may need calibration for the camera and lighting conditions.
