![Architecture](https://img.shields.io/badge/Architecture-Multi--Tier-blue?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Nginx%20%7C%20Flask%20%7C%20PostgreSQL-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-VMware-lightgrey?style=flat-square)
![Network](https://img.shields.io/badge/Network-Segmented-orange?style=flat-square)

# 📌 Trading System Lab (Multi-Tier Architecture)

## 📖 Overview

The **Trading System Lab** is a multi-tier web application architecture designed to simulate an enterprise-style distributed system using segmented virtual networks.

The system allows users to view trading data stored in a PostgreSQL database through a simple web interface. When a user interacts with the frontend dashboard (e.g., clicking **“Load Trades”**), a request is processed across multiple isolated layers before the data is returned to the browser.

At the core of the system, **Nginx acts as a reverse proxy**, serving as the single entry point for all client traffic while the Flask API server processes requests and interacts with the database. Management network allows for direct remote management of the system.

---

## ⭐ Tech Stack

* Frontend: HTML, CSS, JavaScript
* Web Server: Nginx
* Backend: Python (Flask)
* Database: PostgreSQL
* Infrastructure: Virtual Machines, Isolated Networks
* System Tools: systemd, Linux networking

---
## 🖥️ Virtual Machine Inventory

| VM           | Role             | Network(s)                                    |
|--------------|------------------|-----------------------------------------------|
| `web-server` | Nginx / Frontend | Web Network                                |
| `app-server` | Flask API        | API Network                                |
| `db-server`  | PostgreSQL       | Database Network                           |
| `Trader-VM`  | Dashboard testing| Web Network,    |
| `Management-VM`| Management of servers/clients | Management Network                   |



---
## 🎯 Purpose

This lab demonstrates practical skills in:

- Network segmentation across virtual machines
- SQL database configuration and access control
- Separation of frontend, backend, and database layers
- API development and integration using **Python**
- Reverse proxy configuration using Nginx
- Service management using `systemd`
- Debugging distributed system issues across multiple nodes

--- 
## 🔀 System Flow

![Architecture Diagram](assets/Architecture.png)
1. User opens the web application in the browser  
2. User clicks **“Load Trades”**  
3. Browser sends a request to `/api/trades`  
4. Nginx receives the request  
5. Nginx forwards it to the Flask API server 
6. Flask processes the request and queries the database  
7. PostgreSQL returns the requested data  
8. Flask API server formats the response as JSON and returns it
9. Browser displays the trading data in the dashboard

---

## 🌐 Network Design

| Network            | Subnet            | Purpose                     |
|------------------|------------------|----------------------------|
| Web Network       | 192.168.30.0/24  | Web server & client access |
| API Network       | 192.168.35.0/24  | Backend application layer  |
| Database Network  | 192.168.40.0/24  | Data storage layer         |
| Management Network| 192.168.50.0/24  | Administrative access      |

![Topology Diagram](assets/Network-topology.png)

---
## 🏗️ System Architecture

The system is structured into three main layers:

---
### 🌐 Web Layer : Nginx 
Provides a secure interface between external users and internal backend services

- Serves static frontend files (HTML, CSS, JavaScript)
- Acts as a reverse proxy, routing API requests to the Flask API server
- Serves as the single entry point for all client traffic

---

### ⚙️ Application Layer: Flask API server (Flask)
Handles all application logic and API functionality

- Provides REST API endpoints
- Processes incoming requests from Nginx
- Communicates with the PostgreSQL database
- Returns structured JSON responses to the frontend

---

### 🗄️ Data Layer: PostgreSQL server
Stores and manages trading data

- Maintains structured trading datasets
- Is not directly exposed to external users or networks
- Is accessible only through the Flask API server and management network
- Ensures data integrity, consistency and security

---

## 🧠 Key Design Decisions

* Network segmentation was implemented using isolated subnets to reduce attack surface and enforce strict service-to-service communication.
* Database isolation ensures PostgreSQL is not directly exposed, enforcing all access through the API layer for security and consistency.
* Nginx reverse proxy acts as a single entry point, centralizing request routing and hiding backend infrastructure from external exposure.
* Virtual machine separation was used to simulate a realistic distributed production environment with strong service isolation.
* systemd service management ensures reliable startup, process control, and service persistence across system reboots.

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
│   ├── nginx.conf
│   ├── trading.conf
│   ├── index.html
│   ├── style.css
│   └── app.js
├── app-server/
│   ├── README.md
│   ├── app.py
│   ├── requirements.txt
│   └── flask-api.service
├── db-server/
│   ├── README.md
│   ├── schema.sql
│   ├── seed.sql
│   └── pg_hba.conf
└── network/
    ├── README.md
    └── network-design.md
```
---

## 🧠 What I Learned

This project provided hands-on experience with real-world infrastructure and system design concepts, including:

- Configuring SQL database, users and tables
- Setting up reverse proxies with Nginx  
- Configuring REST API
- Managing Linux services with systemd
- Debugging cross-network communication issues  
- Integrating frontend, backend, and database systems  

It also strengthened my ability to troubleshoot complex distributed systems in a structured and systematic way.

---

## 🔮 Future Improvements

- Add authentication (JWT or API keys)
- Implement firewall rules using `iptables` or `nftables`
- Add centralized logging and monitoring (ELK stack)
- Containerize services using Docker
- Introduce load balancing for scalability
- Improve frontend UI/UX design
- Add HTTPS/TLS encryption between services

---

## 📄 Summary

The Trading System Lab demonstrates how a simple web application such as [LAB1](https://github.com/RM1213-ARM/LAB-1-Linux-Networking/tree/main) can evolve into a structured multi-tier distributed system using real-world architecture principles.

By separating services into isolated network layers and deploying them across multiple virtual machines, this project demonstrates key concepts such as scalability, security, maintainability, and infrastructure design.

Overall, it serves as practical experience in building and managing enterprise-style distributed systems.
