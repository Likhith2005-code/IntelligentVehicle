# L4 — Central Dashboard

This is the presentation/dashboard module for the Intelligent Heavy Vehicle Safety system.

## Features

- Live connection to L3 Safety Engine
- Driver monitoring status
- Road monitoring status
- Risk score
- SAFE / WARNING / CRITICAL status
- Controlled braking simulation status
- Hazard-light simulation status
- Risk reasons

## Setup

Open PowerShell in this folder:

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configure L3 address

Open `app.py` and change:

```python
SERVER_URL = "http://127.0.0.1:5000"
```

to the L3 laptop's local IP address, for example:

```python
SERVER_URL = "http://192.168.1.25:5000"
```

## Run

```powershell
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in the browser.

## Important

This dashboard displays simulated emergency responses. It does not control an actual vehicle's braking or lights