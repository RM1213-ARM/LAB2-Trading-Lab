# ⚙️ Application Server — Flask API

## 📖 Overview

The application server runs a Flask-based API on Ubuntu, acting as the backend layer of the system. 

It handles requests from the web server, executes application logic and retrieves data from the PostgreSQL database.

All API requests are received via the web server (Nginx) and handled internally within the API Network.
All API traffic is internal and restricted to the API Network

---

## ⭐ Role in Architecture

| Property   | Value                          |
|-----------|---------------------------------|
| VM Name    | robertapi                      |
| OS         | Ubuntu                         |
| Service    | Flask (Python API)             |
| Network    | API Network                    |
| Gateway    | 192.168.35.1                   |
| IP Address | 192.168.35.20                  |
| Port       | 5000                           |

---

## 📂 Configuration Files

| File               | Purpose |
|--------------------|--------|
| `app.py`           | Main Flask API application |
| `requirements.txt` | Python dependencies |
| `api.service` | systemd service configuration |

---

## ⚙️ Core Responsibilities

- Exposes REST API endpoints (e.g. `/api/trades`)
- Processes incoming requests from Nginx
- Executes application logic
- Queries the PostgreSQL database
- Returns structured JSON responses to the client

---

## 🔁 Request Flow

A typical API request follows this process:

1. Nginx forwards the request to the Flask API
2. Flask processes the request
3. A query is sent to PostgreSQL
4. The database returns results
5. Flask formats the response as JSON
6. Response is returned to Nginx

---

## 🚀 Setup Instructions

### 1. Install system dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip libpq-dev python3-dev -y
```
### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python3 app.py
```
---

## Run as a systemd service
```bash
sudo cp api.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable api
sudo systemctl start api
sudo systemctl status api
```
---

## 🔌 API Endpoint Example

### `GET /api/trades`

Returns trading data from the database.

### Example Response

```json
[
  {
    "id": 1,
    "symbol": "AAPL",
    "price": 150.25
  },
  {
    "id": 2,
    "symbol": "TSLA",
    "price": 720.10
  }
]
```
