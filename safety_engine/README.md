# L3 — Safety Engine + Communication Server

This module is the central decision-making service.

## Responsibilities

- Receive driver-monitoring results from L1
- Receive road-monitoring results from L2
- Calculate a prototype risk score
- Determine SAFE / WARNING / CRITICAL
- Generate simulated controlled-braking and hazard-light states
- Provide the combined status to L4

## Setup

Open PowerShell in this folder:

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```powershell
python server.py
```

The server listens on:

```text
http://0.0.0.0:5000
```

Other laptops should use the L3 laptop's LAN IP, for example:

```text
http://192.168.1.25:5000
```

Do NOT use `0.0.0.0` from the other laptops. They need L3's actual local IP address.

## API

Driver data:

```text
POST /driver
```

Example JSON:

```json
{
  "drowsiness": true,
  "distraction": false,
  "yawning": false
}
```

Road data:

```text
POST /road
```

Example JSON:

```json
{
  "vehicles": 2,
  "people": 0,
  "motorcycles": 1,
  "trucks": 1,
  "hazard": true
}
```

Combined status:

```text
GET /status
```

## Important

Braking and hazard lights are SOFTWARE SIMULATIONS in this prototype. The server does not control a real vehicle.
