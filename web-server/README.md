# 🌐 Web Server — Nginx

## 📖 Overview

The web server runs **Nginx** on Ubuntu and acts as the single entry point for all client traffic.

It serves a static HTML dashboard and reverse proxies API requests to the Flask backend running on the API Network (192.168.35.0/24)

---

## ⭐ Role in Architecture

| Property       | Value                        |
|----------------|------------------------------|
| VM Name        | robertweb                    |
| OS             | Ubuntu                       |
| Service        | Nginx                        |
| Network        | Web Network                  |
| Gateway        | 192.168.30.1                 |
| IP Address     | 192.168.30.10                |
| Listening Port | 80 (HTTP)                    |


---

## 📂 Configuration Files

| File            | Location | Purpose                                      |
|-----------------|----------|----------------------------------------------|
| `nginx.conf`    | `/etc/nginx/nginx.conf` | Main Nginx configuration (global settings) |
| `default.conf`  | `/etc/nginx/sites-available/default` | Virtual host — static files & reverse proxy |
| `index.html`    | `/var/www/html/index.html` | Frontend dashboard (served by Nginx) |

---

## ⚙️ Core Responsibilities

- Serves static HTML dashboard (`index.nginx-debian.html`)
- Acts as a reverse proxy for `/api/*` requests to 
- Routes API traffic to the Flask backend (`http://192.168.35.20:5000`)
- Provides the single external entry point into the system

---

## ➡️ Request Flow

### A typical request to retrieve trading data follows this path:
 ```
Browser                    Nginx                  Flask API              PostgreSQL
  │                          │                        │                      │
  ├─ GET /api/trades ────→                            │                      │
  │                          ├─ Forward to ────→                             │
  │                          │ 192.168.35.20:5000     │                      │
  │                          │                        ├─ SELECT * ────→       
  │                          │                        │ FROM trades          │
  │                          │                         ←─ [rows] ──────       
  │                           ←─ JSON response ──     │                      │
  │←─ [trades table] ─────   │                        │                      │
  │                          │                        │                      │
```
**Detailed steps:**

1. **Client sends request** → `GET http://192.168.30.10/api/trades`
2. **Nginx receives request** on port 80
3. **Nginx evaluates the path:**
   - Matches `location /api/` rule
   - **Strips** `/api` from the URL (due to trailing slash in `proxy_pass`)
4. **Nginx forwards to Flask API Server** → `GET http://192.168.35.20:5000/trades`
   - Includes headers: `X-Real-IP`, `X-Forwarded-For` (preserves client info)
5. **Flask processes request** → Queries PostgreSQL
6. - `Select * FROM trading_sheet`
7. **PostgreSQL returns data** → Flask formats as JSON
8. **Nginx receives response** from Flask
9. **Nginx forwards response** back to browser
10. **Client renders** the trades table in browser
---

## 🔒 Security Considerations

- Backend API server is not reachable from clients
- Only HTTP (Port 80) is exposed externally
- Nginx acts as a controlled gateway to backend services
- No database credentials or backend logic are present on this VM

---

## 🚀 Setup Instructions

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

### 2. Deploy configuration files

```bash
sudo cp default.conf /etc/nginx/sites-available/default
sudo cp nginx.conf /etc/nginx/nginx.conf
```
### 3. Deploy frontend dashboard
```bash
sudo cp index.nginx-debian.html /var/www/html/index.nginx-debian.html
```

### 4. Validate Configuration
```bash
sudo nginx -t
```
Expected output:
nginx: the configuration file syntax is ok
nginx: configuration file test is successful


### 5. Start, Enable and check status of Nginx

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### 6. Test Connectivity

**From any machine with network access to 192.168.30.10:**

```bash
curl http://192.168.30.10

# Should return HTML content of index.html
```

**Open in browser:**
```bash
http://192.168.30.10

# Should see the "Trading Dashboard" with a "Load Trades" button.
```
---

## 🔧 Service Management

```bash
sudo systemctl status nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
```
---
