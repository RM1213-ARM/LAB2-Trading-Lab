# Trading System Lab (Multi-Tier Architecture)
This project is a simple trading dashboard that displays data from a database.

When a user clicks a button in the browser, the system retrieves trade data and displays it on the screen.

---

## What am I designing?
This project is not just a website — it is a multi-tier system, meaning different parts of the application are separated and run on different machines.

The goal is to simulate how real-world systems are built in companies.

Instead of everything running in one place, the system is split into:

A web server (what the user sees)
An API server (handles logic and data processing)
A database (stores data)

---

## Why is it designed this way?
In real systems:

You do NOT want users directly accessing the database
You do NOT want everything running on one machine
You want clear separation between components

This design improves:
Security
Scalability
Maintainability

---

## What each part does
### Web Server (Nginx)
- Serves the website (HTML + JavaScript)
- Acts as a gateway for API requests
- Forwards /api requests to the API server

---

### API Server (Flask)
- Receives requests from the web server
- Processes logic
- Queries the database
- Returns data as JSON

---

### Database (PostgreSQL)
- Stores trading data
- Only accessible by the API server

---

## How the system works (step-by-step)
1. User opens the website
2. User clicks "Load Trades"
3. JavaScript sends request to /api/trades
4. Nginx receives the request
5. Nginx forwards it to the API server
6. Flask API queries the database
7. Database returns data
8. API sends JSON response back
9. Browser displays the data

---

## Network Design
The system is split across multiple networks:

| Network | Purpose |
|--------|--------|
| 192.168.30.0/24 | Web Server & Trading VM |
| 192.168.35.0/24 | API Server |
| 192.168.40.0/24 | Database |
| 192.168.50.0/24 | Management |

This ensures:
- Systems are isolated
- Access can be controlled
- The database is protected

---

## Key Feature: Reverse Proxy
The web server uses a **reverse proxy**:
/api --> forwarded to API server

This means:
The browser never talks directly to the API
All traffic goes through the web server

---

Technologies Used
Nginx (web server + reverse proxy)
Flask (Python API)
PostgreSQL (database)
Linux VMs
systemd (service management)

---
## Challenges I Solved
During development, I encountered and fixed:

API not reachable (502 Bad Gateway)
Incorrect network binding (127.0.0.1 vs 0.0.0.0)
Missing Python dependencies
Service startup issues (systemd)
Frontend JavaScript errors

---

## What I Learned
How to design a multi-tier architecture
How reverse proxies work
How frontend, backend, and database interact
Debugging across multiple systems
Service management with systemd

---

## Future Improvements
Add authentication (JWT / API keys)
Restrict API access with firewall rules
Add monitoring and logging
Use Docker for deployment

---

## Summary
This project demonstrates how a simple application can be transformed into a structured, scalable system using real-world architecture principles.
