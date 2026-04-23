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
| Port       | 5432 (default)                    |

---

## 📂 Configuration Files

| File           | Location | Purpose |
|---|---|---|
| `postgresql.conf` | `/etc/postgresql/16/main/postgresql.conf` | Configures server settings (port, network binding, performance) |
| `pg_hba.conf` | `/etc/postgresql/16/main/pg_hba.conf` | Defines authentication and access rules (critical for security) |

## ⚙️ Database Responsibilities

PostgreSQL is responsible for:

- **Data storage**: Storing structured trading data in tables with ACID guarantees
- **Query execution**: Processing SQL queries (SELECT, INSERT, UPDATE, DELETE)
- **Data integrity**: Enforcing constraints (primary keys, unique constraints, foreign keys)
- **Concurrent access**: Managing multiple simultaneous connections safely
- **Authentication**: Validating user credentials before allowing connections
- **Authorization**: Controlling which users can access which databases and tables

---

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
# Allow API Server (read-only)
host    trading_sheet   trader          192.168.35.20/32    md5

# Allow Management Network (administration)
host    trading_sheet   trader          192.168.50.10/32    md5
```

**Why `/32` instead of `/24`?**

- `/32` = Single IP address (192.168.35.20 exactly) — allows **only that one machine** (Least privilege)

---

## 🔁 Data Flow

1. **Flask API** (192.168.35.20) initiates a connection to PostgreSQL
2. PostgreSQL checks `pg_hba.conf` —-> is 192.168.35.20 allowed? 
3. PostgreSQL validates the username (`trader`) and password (`traderpass`)
4. PostgreSQL grants access to the `trading_sheet` database
5. Flask executes: `SELECT * FROM trades;`
6. PostgreSQL returns the result set
7. Flask formats the data as JSON
8. JSON response travels back through Nginx to the browser





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
listen_addresses = '*'
port = 5432
```

This tells PostgreSQL to:
- Listen on all network interfaces (not just localhost)
- Use port 5432 (default)

**Why not just localhost?**
- If PostgreSQL only listened on localhost (127.0.0.1), only connections from the same machine would be allowed
- We need the API server (192.168.35.20) to connect from a different machine
- But we'll restrict which IPs can actually authenticate via `pg_hba.conf`

### 6. Configure Host-Based Authentication

**File: `/etc/postgresql/16/main/pg_hba.conf`**

Find the section with IPv4 local connections and **update these lines** (change `/24` to `/32`):
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

