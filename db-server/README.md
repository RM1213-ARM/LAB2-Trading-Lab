# 🗄️ Database Server — PostgreSQL

## 📖 Overview

The database server runs PostgreSQL and stores all trading data used by the system.

It is placed in a separate network layer and is **not directly accessible from the web layer**. Access is controlled through the API server and management network to ensure security and data integrity.

---

## ⭐ Role in Architecture

| Property   | Value                              |
|-----------|------------------------------------|
| VM Name    | robertdatabase                     |
| OS         | Ubuntu                            |
| Service    | PostgreSQL                        |
| Network    | Database Network (192.168.40.0/24) |
| IP Address | 192.168.40.20                    |

---

## 📂 Files

| File           | Purpose |
|---------------|--------|
| `schema.sql`  | Defines database structure (tables, columns, types) |
| `seed.sql`    | Inserts initial/sample data into the database |
| `pg_hba.conf` | Controls database access permissions and security rules |

---

## 🏗️ Database Structure

### `schema.sql`

This file defines the structure of the database.

It is used to:
- Create tables
- Define columns and data types
- Organize how trading data is stored

Example: a `trades` table stores trading records such as symbol and price.

---

## 🌱 Seed Data

### `seed.sql`

This file inserts initial data into the database.

It is used to:
- Populate the database with sample trading records
- Allow the API server to return meaningful results immediately
- Help with testing and development

---

## 🔐 Access Control

### `pg_hba.conf`

This file defines who is allowed to connect to the PostgreSQL database.

It is used to:
- Restrict access to only the API server network
- Block direct external access to the database
- Define authentication rules for users

This ensures the database is **not publicly exposed**.

---

## 🔁 Data Flow

1. API server sends SQL query to PostgreSQL  
2. Database processes the request  
3. Results are returned to the API server  
4. API formats data into JSON  
5. Response is sent to the frontend  

---

## ⚙️ Setup Instructions

### 1. Install PostgreSQL

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib -y

### 2. Create the database
sudo -u postgres psql
CREATE DATABASE trading_sheet;
