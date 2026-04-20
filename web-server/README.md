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

## 📂 Files

| File            | Purpose                                      |
|-----------------|----------------------------------------------|
| `nginx.conf`    | Main Nginx configuration                     |
| `default.conf`  | Virtual host — static files & reverse proxy  |
| `index.html`    | Frontend dashboard                           |


---

## ➡️ Request Flow

1. Client sends HTTP `GET` request to the web server
2. Nginx evaluates the request path:
   - `/` → serves static frontend files
   - `/api/*` → reverse proxies to Flask API at `192.168.35.20`
3. Flask processes the request and returns a response
4. Nginx forwards the response back to the client

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

## 🔧 Service Management

```bash
# Start Nginx
sudo systemctl start nginx

# Enable on boot
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx

# Reload config without downtime
sudo systemctl reload nginx
```

---
