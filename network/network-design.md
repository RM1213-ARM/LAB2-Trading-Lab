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

| Server        | IP Address       | Connected Networks        |
|--------------|------------------|--------------------------|
| Web Server   | 192.168.30.10    | Web Network              |
| API Server   | 192.168.35.20    | API Network              |
| DB Server    | 192.168.40.20    | Database Network         |
| Trader VM    | 192.168.30.20    | Web Network              |
| Management VM | 192.168.50.10   | Management Netowrk       |

---

## 🔁 Communication Flow

1. User connects to the Web Server (Nginx)
2. Nginx forwards API requests to the API Server
3. API Server queries PostgreSQL
4. Database responds to API Server
5. API returns data to Web Server
6. Web Server returns response to user

---

## 🔐 Security Design

- Database is NOT accessible from the Web Network  
- API server is the only component that communicates with the database  
- Network segmentation reduces attack surface  
- Access is restricted using `pg_hba.conf`  

---

## 🖼️ Network Diagram

![Network Topology](/assets/Network-topology.png)
