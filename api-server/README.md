# ⚙️ Application Server — Flask API

## 📖 Overview

The application server runs a Flask-based API on Ubuntu, acting as the backend layer of the system. It processes incoming requests from the web server, executes application logic, and retrieves data from the PostgreSQL database.

All API requests are received via the web server (Nginx) and handled internally within the API Network.

---

## ⭐ Role in Architecture

| Property   | Value                          |
|-----------|--------------------------------|
| VM Name    |`robertapi`                    |
| OS         | Ubuntu                         |
| Service    | Flask (Python API)             |
| Network    | API Network (192.168.35.0/24)  |
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
7. Response is sent back to Nginx  
8. Nginx returns the response to the client  

---

## ⚙️ Application Behaviour

- REST API — exposes endpoints such as `/api/trades`  
- Data processing — handles request logic and formatting  
- Database interaction — queries PostgreSQL for trading data  
- JSON responses — returns structured data to the frontend  

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
