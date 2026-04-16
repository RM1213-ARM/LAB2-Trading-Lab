# ⚙️ Application Server — Flask API

## 📖 Overview

The application server runs a Flask-based API on Ubuntu, acting as the backend layer of the system. It processes incoming requests from the web server, executes application logic, and retrieves data from the PostgreSQL database.

All API requests are received via the web server (Nginx) and handled internally within the API Network.

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

---

## 📂 Files

| File               | Purpose |
|--------------------|--------|
| `app.py`           | Main Flask API application |
| `requirements.txt` | Python dependencies |
| `flask-api.service` | systemd service configuration |

---

## ➡️ Request Flow

1. Flask receives the request (e.g. `GET /api/trades`)  
2. Application logic is executed  
3. Flask queries the PostgreSQL database 
4. Database returns results  
5. Flask formats the data as JSON  
6. Response is sent back to Nginx (via Router)

---

## ⚙️ Application Behaviour

- REST API — exposes endpoints such as `/api/trades`  
- Request handling - processes incoming HTTP requests from Nginx
- Data processing — handles request logic and formatting  
- Database access — queries PostgreSQL for trading data  
- JSON responses — returns structured data to the frontend  

---

## 📦 Core Dependencies

The API Server consists of the following components:

### 1. Flask 
A lightweight Python web framework used to build the REST API

Capabilities:
- Define API routes (e.g `/apt/trades`)
- Handle HTTP requests from the web server
- Return JSON responses to frontend

### 2. Flask-CORS
Enables Cross-Origin Resource Sharing 

It is required because:
- Frontend and backend run on different servers
- Browsers usually block cross-origin requests by default

### 3. psycopg2-binary 
A PostgreSQL adapter for Python

Used to:
- Execute SQL queries
- Retrieve data from the database
- Return results to the API layer

                     
---

## 🚀 Setup Instructions

### 1. Install system dependencies
bash
sudo apt-get update
sudo apt-get install python3 python3-pip libpq-dev python3-dev -y

### 2. Install Python dependencies
pip install -r requirements.txt

### 3. Run the application
python3 app.py

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
