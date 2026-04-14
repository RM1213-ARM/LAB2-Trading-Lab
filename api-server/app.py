#The core backend application of the system.

#This file defines a Flask-based REST API that:
#- Handles incoming HTTP requests from the web server
#- Establishes a connection to the PostgreSQL database
#- Executes SQL queries to retrieve trading data
#- Converts database results into JSON format
#- Returns structured responses to the client

#It acts as the **application logic layer**, ensuring that the frontend never interacts directly with the database.

from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="192.168.40.20",
            database="trading_sheet",
            user="trader",
            password="traderpass"
        )
        return conn
    except Exception as e:
        print("DB connection error:", e)
        return None

@app.route('/trades')
def trades():
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}, 500

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT * FROM trades;")
        rows = cur.fetchall()

        result = [dict(row) for row in rows]

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        cur.close()
        conn.close()

    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
