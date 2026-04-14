# 🌐 Web Server — Nginx

## 📖 Overview

The web server runs **Nginx** on Ubuntu, acting as the single entry point for all client traffic. It serves the static frontend files and reverse proxies all `/api/*` requests to the Flask API server on the API Network.

---

## ⭐ Role in Architecture

| Property       | Value                        |
|----------------|------------------------------|
| VM Name        | `web-server`                 |
| OS             | Ubuntu                       |
| Service        | Nginx                        |
| Network        | Web Network (192.168.30.0/24)|
| IP Address     | 192.168.30.x                 |

---

## 📂 Files

| File            | Purpose                                      |
|-----------------|----------------------------------------------|
| `nginx.conf`    | Main Nginx configuration                     |
| `trading.conf`  | Virtual host — static files & reverse proxy  |
| `index.html`    | Frontend dashboard                           |


---

## ➡️ Request Flow

1. Client sends a `GET` request to the web server
2. Nginx checks the request path:
   - `/` → serves static frontend files
   - `/api/*` → reverse proxies to Flask API at `192.168.35.20`
3. Response is returned to the client

---

## ⚙️ Nginx Behaviour

- **Static files** — serves `index.html`, `style.css`, and `app.js` directly
- **Reverse proxy** — forwards `/api/*` requests to `http://192.168.35.20:5000`
- **Single ingress** — backend infrastructure is never exposed directly to clients

---

## 🔒 Security Considerations

- Backend API server is not reachable from the Web Network directly
- Nginx acts as a barrier — clients only ever communicate with the web server
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

## 📁 Files in This Directory

```
web-server/
├── README.md
├── nginx.conf
├── trading.conf
├── index.html
├── style.css
└── app.js
```
