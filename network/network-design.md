# 🌐 Network Design

## 📖 Overview

This document describes the network architecture of the Trading System Lab.  
Each layer of the application is seperated at the network level, enforcing controlled communication between services.

---
![Network Topology](/assets/Topology.png)


## 🧩 Network Segmentation

| Network            | Subnet            | Purpose                     |
|------------------|------------------|----------------------------|
| Web Network       | 192.168.30.0/24  | Client access & web server |
| API Network       | 192.168.35.0/24  | Application layer  |
| Database Network  | 192.168.40.0/24  | Database services    |
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

A dedicated Router VM connects all isolated network segments and acts as the default gateway for each subnet.

- Each network uses the Router  as its gateway
- The Router has one network interface per subnet
- IP forwarding is enabled to allow inter-network communication

---

## 🔁 Communication Flow
A typical request (`GET /api/trades`) flows through the system as follows:

1. Client sends request to the Web Server (Nginx)
2. Nginx forwards the request to API server (via Router)
3. API Server processes the request and queries the Database (via Router)
7. Database responds to API Server (via Router)
8. API returns data to Web Server (via Router)
9. Web Server returns response to client

---

## 🔐 Security Design

- Network segmentation isolates each system layer
- Database is not accessible from the Web Network
- Database access is further restricted in `pg_hba.conf`
- All inter-network traffic passes through the Router 
- Access between networks are controlled via firewall rules on the router
- Only the API server and management network are permitted to communicate with PostgreSQL database  

---
