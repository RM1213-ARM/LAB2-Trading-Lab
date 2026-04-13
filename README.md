# Trading System Lab (Multi-Tier Architecture)

## Overview

This project is a multi-tier trading system designed to simulate a real-world enterprise architecture.

It demonstrates how a frontend application, backend APi and dataase interact across segmented networks using a reverse proxy.

### Technology Used
- Nginx (Web server & Reverse Proxy)
- Flask (Python API)
- PostgreSQL (Database)
- Linux (Multiple VMs)
- systemd (Service managemnet)

---

## Architecture


### Key Concept
All API traffic is routed through Nginx using "/api", meaning the browser never directly communicates with the API server.

## Network Segmentation

| Network | Purpose |
|--------|--------|
| 192.168.30.0/24 | Web Server & Trading VM |
| 192.168.35.0/24 | API Server |
| 192.168.40.0/24 | Database Server |
| 192.168.50.0/24 | Management |

### Security Design
- Database is only accessible by the API server
- API is accessed through the web server (reverse proxy)
- Systems are separated across subnets

---

## Features
Multi-VM architecture
Reverse proxy routing (/api → API server)
REST API built with Flask
PostgreSQL database integration
Interactive web dashboard
Persistent API service using systemd
Network segmentation between layers

---

## Request Flow
User clicks "Load Trades" on the web interface
JavaScript sends request to /api/trades
Nginx receives the request on the Web VM
Nginx forwards request to API server (192.168.35.20:5000)
Flask API processes request and queries PostgreSQL
Database returns data
API returns JSON response
Frontend displays the data

---

## Troubleshooting (Key Learnings)
During development, several real-world issues were encountered and resolved:

502 Bad Gateway (API not reachable)
Flask binding issues (127.0.0.1 vs 0.0.0.0)
Missing Python dependencies (flask, flask-cors, psycopg2)
systemd service failures
Frontend JavaScript errors (loadTrades not defined)

---

## What I Learned
Designing a multi-tier architecture
Implementing reverse proxy with Nginx
Debugging distributed systems across multiple machines
Managing backend services with systemd
Integrating frontend, API, and database layers
Understanding network segmentation and service isolation

---

## Future Improvements
Implement API authentication (JWT / API key)
Restrict API access using firewall rules (only Web → API)
Add logging and monitoring
Containerize services with Docker
Add HTTPS (TLS encryption)

---

## Summary
This project demonstrates how to build and troubleshoot a distributed system using industry-relevant architecture patterns. It reflects real-world challenges in networking, backend development, and system design.
