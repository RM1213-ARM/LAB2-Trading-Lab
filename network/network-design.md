# 🌐 Network Design

## 📖 Overview

This document describes the network architecture of the Trading System Lab.  
The system is divided into isolated networks to simulate a secure, enterprise-style infrastructure.

---

## 🧩 Network Segmentation

| Network            | Subnet            | Purpose                     |
|------------------|------------------|----------------------------|
| Web Network       | 192.168.30.0/24  | Client access & web server |
| API Network       | 192.168.35.0/24  | Backend application layer  |
| Database Network  | 192.168.40.0/24  | Database communication     |
| Management Network| 192.168.50.0/24  | Administrative access      |

---

## 🖥️ VM Placement

| Server         | IP Address       | Connected Networks        |
|---------------|------------------|--------------------------|
| Router VM     | 192.168.30.1     | Web Network              |
|               | 192.168.35.1     | API Network              |
|               | 192.168.40.1     | Database Network         |
|               | 192.168.50.1     | Management Network       |
| Web Server    | 192.168.30.10    | Web Network              |
| API Server    | 192.168.35.20    | API Network              |
| DB Server     | 192.168.40.20    | Database Network         |
| Trader VM     | 192.168.30.20    | Web Network              |
| Management VM | 192.168.50.10    | Management Network       |

---

## 🔌 Service Ports

| Service     | Port |
|------------|------|
| HTTP (Nginx) | 80  |
| Flask API    | 5000 |
| PostgreSQL   | 5432 |
| SSH          | 22  |

---
## 🔀 Routing & Connectivity

A dedicated Router VM connects all isolated network segments.

- Each subnet uses the Router VM as its default gateway
- The router has one network interface per subnet
- IP forwarding is enabled to allow inter-network communication

All traffic between system layers flows through the router:

- Web Server → API Server traffic is routed via the Router VM
- API Server → Database traffic is routed via the Router VM

This design centralises control and enables future firewall enforcement.

---

## 🔁 Communication Flow
This section describes how the application request (e.g. `GET /api/trades`) traverses the network infrastructure.

1. User connects to the Web Server (Nginx)
2. Nginx sends API request to Router VM (Default Gateway)
3. Router forwards request to API Server
4. API Server processes the request
5. API Server sends database query via the Router
6. Router forwards request to Database Server
7. Database responds to API Server (via Router)
8. API returns data to Web Server (via Router)
9. Web Server returns response to user

---

## 🔐 Security Design

- Network-segmentation isolates each system layer
- Database is not accessible from the Web Network
- Database access is further restricted in `pg_hba.conf`
- All inter-network traffic passes through the Router VM
- Access between networks can be controlled via firewall rules on the router
- Only API server and management network are permitted to communicate with SQL database  

---

## 🖼️ Network Diagram

![Network Topology](/assets/Network-topology.png)
