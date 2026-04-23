# 🗄️ Database Server — PostgreSQL

## 📖 Overview

The database server runs PostgreSQL and stores all trading data used by the system.

It is deployed in an isolated Database Network and is not directly accessible from the **Web network**. Access is restricted to the API Server and Management Network to ensure security and data integrity.

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
| Port       | 5432                              |

---

## 📂 Configuration Files

| File           | Location | Purpose |
|---|---|---|
| `postgresql.conf` | `/etc/postgresql/16/main/postgresql.conf` | Configures server settings (port, network binding, performance) |
| `pg_hba.conf` | `/etc/postgresql/16/main/pg_hba.conf` | Defines authentication and access rules (critical for security) |

## ⚙️ Database Responsibilities

PostgreSQL is responsible for:

- Storing structured trading data
- Handling authentication and autorization
- Managing concurrent database connections 
- Processing SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Enforcing data integrity (primary keys, constraints)


## 📊 Database Schema

### Database: `trading_sheet`

### Table: `trades`

| Column | Type | Constraints | Purpose |
|--------|------|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique identifier for each trade (auto-incrementing) |
| `symbol` | VARCHAR(10) | NOT NULL | Stock ticker symbol (e.g., AAPL, GOOG) |
| `price` | NUMERIC(10,2) | NOT NULL | Trade price with 2 decimal places |

### Sample Data

```sql
INSERT INTO trades (symbol, price) VALUES
  ('AAPL', 172.50),
  ('GOOG', 2810.30),
  ('TSLA', 720.10);
```

---

## 🔐 Security: Access Control

Database access is restricted using `pg_hba.conf` (PostgreSQL Host-Based Authentication).

### Users

| Username | Password | Privileges | Purpose |
|---|---|---|---|
| `postgres` | (system) | Superuser | Administrative access (only for setup) |
| `trader` | `traderpass` | SELECT on trades table | API server read-only access |

**Important:** The `trader` user can only **SELECT** (read) data, not INSERT/UPDATE/DELETE. This prevents accidental or malicious data modifications from the application layer.

### Access Rules 

```conf
# TYPE  DATABASE        USER            ADDRESS             METHOD
# Allow API Server & Management VM
host    trading_sheet   trader          192.168.35.20/32    md5
host    trading_sheet   trader          192.168.50.10/32    md5
```

- `/32` = Ensures only specific IP addresses are allowed (least priviledge)

---

## 🔁 Data Flow

1. **Flask API** (192.168.35.20) initiates a connection to PostgreSQL
2. PostgreSQL validates `pg_hba.conf` rules 
3. PostgreSQL validates the username (`trader`) and password (`traderpass`)
4. PostgreSQL grants access to the `trading_sheet` database
5. Query is executed: `SELECT * FROM trades;`
6. PostgreSQL returns results to Flask API Server
7. Flask formats the response as JSON
8. Data is sent back through Nginx to the client

---

## ⚙️ Setup Instructions

### 1. Install PostgreSQL
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib -y 
```
### 2. Start and enable service
```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```
### 3. Verify it's running:
```bash
sudo systemctl status postgresql
```
### 4. Create Database and User

Log in as the PostgreSQL system user:
```bash
sudo -u postgres psql
```
Inside the PostgreSQL prompt (`postgres=#`), run:

```sql
-- Create the database
CREATE DATABASE trading_sheet;

-- Create a read-only user
CREATE USER trader WITH ENCRYPTED PASSWORD 'traderpass';

-- Grant connection permission to the database
GRANT CONNECT ON DATABASE trading_sheet TO trader;

-- Switch to the database
\c trading_sheet

-- Create the trades table
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

-- Insert sample data
INSERT INTO trades (symbol, price) VALUES
  ('AAPL', 172.50),
  ('GOOG', 2810.30),
  ('TSLA', 720.10);

-- Grant read-only access to the trader user
GRANT SELECT ON trades TO trader;

-- Exit PostgreSQL
\q
```


### 5. Configure Network Binding

**File: `/etc/postgresql/16/main/postgresql.conf`**

```conf
listen_addresses = '*'             #listen on all network interfaces
port = 5432                        #listen on port 5432
```

We will restrict which specific IPs can authenticate via `pg_hba.conf`

### 6. Configure Host-Based Authentication

**File: `/etc/postgresql/16/main/pg_hba.conf`**

```
```conf
host    trading_sheet    trader    192.168.35.20/32   md5
host    trading_sheet    trader    192.168.50.10/32   md5
```

### 7. Apply Configuration Changes

Restart PostgreSQL to load the new configuration:

```bash
sudo systemctl restart postgresql
```

