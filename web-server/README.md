# 🌐 Web Server — Nginx

## 📖 Overview

The web server runs **Nginx** on Ubuntu, acting as the single entry point for all client traffic. It serves the static frontend files and reverse proxies all `/api/*` requests to the Flask API server on the API Network (192.168.35.0/24)

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

## ➡️ Request Flow

### Scenario: User clicks "Load Trades" button
 ```
Browser                    Nginx                   Flask API              PostgreSQL
  │                          │                         │                      │
  ├─ GET /api/trades ────→ │                         │                      │
  │                          ├─ Forward to ────→     │                      │
  │                          │ 192.168.35.20:5000    │                      │
  │                          │                        ├─ SELECT * ────→     │
  │                          │                        │ FROM trades         │
  │                          │                        │←─ [rows] ──────     │
  │                          │←─ JSON response ──     │                      │
  │←─ [trades table] ─────  │                        │                      │
  │                          │                        │                      │
```
**Detailed steps:**

1. **Browser sends request** → `GET http://192.168.30.10/api/trades`
2. **Nginx receives request** on port 80
3. **Nginx evaluates the path:**
   - Matches `location /api/` rule
   - **Strips** `/api` from the URL (due to trailing slash in `proxy_pass`)
4. **Nginx forwards to Flask** → `GET http://192.168.35.20:5000/trades`
   - Includes headers: `X-Real-IP`, `X-Forwarded-For` (preserves client info)
5. **Flask processes request** → Queries PostgreSQL
6. **PostgreSQL returns data** → Flask formats as JSON
7. **Nginx receives response** from Flask
8. **Nginx forwards response** back to browser
9. **Browser renders** the trades table

---

## ⚙️ Nginx Behaviour

- **Static files** — serves `index.html`, `style.css`, and `app.js` directly
- **Reverse proxy** — forwards `/api/*` requests to `http://192.168.35.20:5000`
- **Single ingress** — backend infrastructure is never exposed directly to clients

---

## 🔒 Security Considerations

- Backend API server is not reachable from the Web Network directly
- Nginx acts as a barrier — clients only ever communicate with the web server
- Only HTTP (port 80) is exposed externally.
- No database credentials or backend logic are present on this VM

---

## 🚀 Setup Instructions

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

### 2. Replace the Virtual Host Configuration

Copy your `default.conf` to:

```bash
sudo cp default.conf /etc/nginx/sites-available/default
```

### 3. Place Frontend Files

Copy your `index.html` to the web root:

```bash
sudo cp index.html /var/www/html/index.html
```

If you have CSS or JavaScript files:
```bash
sudo cp style.css /var/www/html/style.css
sudo cp app.js /var/www/html/app.js
```

### 4. Validate Nginx Configuration

Before restarting, verify the syntax is correct:

```bash
sudo nginx -t
```

**Expected output:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

If there are errors, fix them before continuing!

### 5. Start and Enable Nginx

```bash
# Start the service
sudo systemctl start nginx

# Enable on boot
sudo systemctl enable nginx

# Verify it's running
sudo systemctl status nginx
```

### 6. Test Connectivity

**From any machine with network access to 192.168.30.10:**

```bash
# Test static file serving
curl http://192.168.30.10

# Should return HTML content of index.html
```

**Open in browser:**
```
http://192.168.30.10
```

You should see the "Trading Dashboard" with a "Load Trades" button.

---

## 🔧 Service Management

```bash
# View current status
sudo systemctl status nginx

# Start Nginx
sudo systemctl start nginx

# Stop Nginx
sudo systemctl stop nginx

# Restart (stops then starts)
sudo systemctl restart nginx

# Reload configuration without downtime
# This gracefully restarts only workers, keeps connections alive
sudo systemctl reload nginx

# Enable auto-start on boot
sudo systemctl enable nginx

# Disable auto-start on boot
sudo systemctl disable nginx
```

---
