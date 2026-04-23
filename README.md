![Architecture](https://img.shields.io/badge/Architecture-Multi--Tier-blue?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Nginx%20%7C%20Flask%20%7C%20PostgreSQL-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-VMware-lightgrey?style=flat-square)
![Network](https://img.shields.io/badge/Network-Segmented-orange?style=flat-square)

# 📌 Trading System Lab — Multi-Tier Architecture

## 📖 Overview

The **Trading System Lab** is a multi-tier web application built in VMware, simulating an enterprise-style distributed system across segmented virtual networks.

Users can view trading data stored in a PostgreSQL database through a simple web dashboard. When a user clicks **"Load Trades"**, the request travels across multiple isolated network layers before data is returned to the browser — mimicking real production architecture patterns.

**Nginx** acts as the single entry point and reverse proxy, routing traffic to a **Flask API** server, which in turn queries the database. A dedicated management network enables direct administrative SSH access to all VMs.

This system is fully segmented across multiple virtual networks, enforcing strict separation between presentation, application, and data layers.

---

## ⭐ Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Frontend       | HTML, CSS, JavaScript             |
| Web Server     | Nginx (reverse proxy)             |
| Backend        | Python (Flask)                    |
| Database       | PostgreSQL                        |
| Infrastructure | VMware, Isolated Virtual Networks |
| System Tools   | systemd, Linux networking         |

---

## ➡️ System Flow

![Architecture Diagram](assets/Architecture.png)

1. User opens the web application (browser)
2. User clicks **"Load Trades"** button on UI
3. Browser sends a `GET` request to `/api/trades`
4. **Nginx** receives the request on the Web Network
5. Nginx reverse-proxies the request to the Flask API server
6. **Flask** processes the request and queries PostgreSQL database
7. **PostgreSQL** returns the requested trading records to Flask API
8. Flask formats the response as JSON and returns it to Nginx
9. Nginx forwards the response back to the browser
10. The dashboard renders the trading data

---

## 🌐 Network Design

The system is divided into multiple isolated network segments to separate the web, API, and database layers.  
This ensures controlled communication between services and reduces the attack surface.

For a detailed breakdown of subnets, VM placement, and security design, see:  
👉 [Network Design](network/network-design.md)

![Topology Diagram](assets/Topology.png)

---
# 🧩 Architecture Style

This system follows a three-tier architecture pattern with strict network segmentation:

- **Presentation Layer** (Nginx + Frontend)
- **Application Layer** (Flask API)
- **Data Layer** (PostgreSQL)

Each layer is isolated in a separate subnet and communicates only through controlled network paths.

---

### 🌐 Web Layer — Nginx
Provides a secure interface between external users and internal backend services.

- Serves static frontend files (HTML, CSS, JavaScript)
- Acts as a reverse proxy, routing `/api/*` requests to the Flask API server
- Single entry point for all client traffic — backend infrastructure is never exposed directly

---

### ⚙️ Application Layer — Flask API
Handles all business logic and API functionality.

- Processes requests forwarded from Nginx
- Exposes REST API endpoints (e.g. `GET /api/trades`)
- Queries PostgreSQL and returns structured JSON responses
- Isolated on its own network segment — not reachable directly from clients

---

### 🗄️ Data Layer — PostgreSQL
Stores and manages all trading data.

- Maintains structured trading datasets
- Not exposed to the Web Network or external clients
- Enforces data integrity, consistency, and security
- Accessible only via the Flask API server and management VM

---

## 🧠 Key Design Decisions & Security Considerations

- **Single ingress point**: All traffic enters through Nginx
- **Service isolation**: Each tier runs on a separate subnet
- **No direct database access**: API mediates all database queries
- **Least privilege design**: Services only access what they require
- **systemd service management**: Ensures services persist across reboots 
- **Management network separation**: Admin access is isolated from production traffic 
- **Database isolation**: The API mediates all database access, preventing direct exposure

---
## 🎯 Purpose & Demonstrated Competencies

This project demonstrates:

- Managing services using systemd
- Designing a multi-tier distributed system
- Building a REST API using Python and Flask
- Debugging cross-network communication issues
- Implementing reverse proxy routing with Nginx
- Configuring PostgreSQL with secure access controls
- Integrating frontend, backend, and database layers
- Configuring network segmentation in a virtualised environment

---

## 🔮 Future Improvements

- JWT or API **key authentication** 
- **Load balancing** at the web layer
- **TLS encryption** between all layers
- **Conainerise** services using Docker
- Role-Based Access Control **(RBAC)** 
- Centralised **audit logging** (ELK stack)
- Introduce **monitoring** with Prometheus + Grafana

---

## 🔗 Component Documentation

- 🌐 [Web Server](web-server/README.md)
- ⚙️ [API Server](api-server/README.md)
- 🗄️ [Database Server](db-server/README.md)
- 🌐 [Network Design](network/network-design.md)
- 


---

## 📁 Repository Structure

```
trading-system-lab/
├── README.md
├── assets/
│   ├── Architecture.png
│   └── Network-topology.png
├── web-server/
│   ├── README.md
│   ├── default.conf
│   ├── index.nginx-debian.html
│   ├── nginx.conf  
├── api-server/
│   ├── README.md
│   ├── api.service
│   ├── app.py
│   └── requirements.txt
├── db-server/
│   ├── README.md
│   ├── pg_hba.conf
│   ├── postgresql.conf
└── network/
    ├── README.md
    └── network-design.md
```
---

