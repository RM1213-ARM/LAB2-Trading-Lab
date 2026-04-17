# 🗄️ Database Server — PostgreSQL

## 📖 Overview

The database server runs PostgreSQL and stores all trading data used by the system.

It is placed in a separate network layer and is not directly accessible from the **Web network**. Access is allowed from the API Server and controlled by the management network to ensure security and data integrity.

---

## ⭐ Role in Architecture

| Property   | Value                             |
|------------|-----------------------------------|
| VM Name    | robertdatabase                    |
| OS         | Ubuntu                            |
| Service    | PostgreSQL                        |
| Network    | Database Network                  |
| Gateway    | 192.168.40.1                      |
| IP Address | 192.168.40.20                     |

---

## 📂 Files

| File           | Purpose |
|---------------|--------|
| `postgresql.conf` | Configures server settings (port, network binding, performance)|
| `pg_hba.conf` | Defines authentication and access rules|
---
## 🔐 Access Control

Database access is restricted using `pg_hba.conf`.

- Only the API Server is allowed to connect to PostgreSQL  
- Management network access is permitted for administration  
- All other connections are denied  

This ensures the database is not publicly exposed.

---

## 🔁 Data Flow

1. PostgreSQL receives a SQL query from the API Server  
2. The query is parsed and executed  
3. Data is retrieved or modified within the database  
4. Results are returned to the API Server

---

## ⚙️ Setup Instructions

### 1. Install PostgreSQL
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib -y 
```
### 2. Enable and start service
```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```
### 3. Enter postgres user
```bash
sudo -i -u postgres
psql
```
### 4. Create database and user

```sql
  CREATE DATABASE trading_sheet;
  CREATE USER trader WITH ENCRYPTED PASSWORD 'traderpass';
  GRANT ALL PRIVILEGES ON DATABASE trading_sheet TO trader;
  \q
```

### 5. Connect to the database
```sql
\c trading_sheet
```

### 6. Create table

```sql
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price NUMERIC
);
```

### 7. Insert sample data 
```sql
INSERT INTO trades(symbol, price)
    VALUES 
  ('AAPL', 172.5),
  ('GOOG', 2810.3);
   \q
```

### 8. Configure network access
```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```
```conf
listen_addresses = '*'
```
```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```
```conf
host    trading_sheet    trader    192.168.40.0/24    md5
host    trading_sheet    trader    192.168.50.0/24    md5
```
### 9. Restart PostgreSQL service
```bash
sudo systemctl restart postgresql
```
