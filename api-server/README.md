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

1. Nginx forwards `/api/*` requests to the Flask API server 
2. Flask receives the request (e.g. `GET /api/trades`)  
3. Application logic is executed  
4. Flask queries the PostgreSQL database 
5. Database returns results  
6. Flask formats the data as JSON  
7. Response is sent back to Nginx (via Router)
8. Nginx returns the response to the client  

---

## ⚙️ Application Behaviour

- REST API — exposes endpoints such as `/api/trades`  
- Data processing — handles request logic and formatting  
- Database interaction — queries PostgreSQL for trading data  
- JSON responses — returns structured data to the frontend  

---

Consists of 3 parts:

1. Flask : a lightweight Python web framework that runs the REST API.

Allows the user to:
- Create API routes (e.g `/apt/trades`)
- Handle requests from the web server
- Send responses to frontedn in JSON format

2. Flask-CORS: Allows frontend (browser) to talk to the API Server

It is required because:
- Frontend and backend run on different servers
--> Browsers usually block cross-origin requests by default

3. psycopg2-binary: a PostgreSQL adapter used to connect Python to database

Allows the API Server to:
- Run SQL queries
- Get data from database
- Send results to the frontend

                     
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
