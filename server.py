from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_NAME = "budget_manager.db"

def init_db():
    connection = sqlite3.connect(DB_NAME) # Open a connection to the DB named "budget_manager.db"
    cursor = connection.cursor() # Creates a cursor/tool that lets you send commands(SELECT,INSERT,...) to the DB.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit() # Save changes to the DB
    connection.close()  # Close the connection to the DB

# Old Way @app.route('/api/health', methods=["GET"])
@app.get('/api/health')
def health_check():
    return jsonify({
        "status": "OK"
    }), 200

# ---------- USERS ----------
@app.post('/api/users')
def register():
    new_user = request.get_json()
    print(new_user)

    username = new_user["username"]
    password = new_user["password"]

    connection = sqlite3.connect(DB_NAME) # Open a connection to the DB named "budget_manager.db"
    cursor = connection.cursor() # Creates a cursor/tool that lets you send commands(SELECT,INSERT,...) to the DB.
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Executes SQL Statement
    connection.commit() # Saves the changes
    connection.close()  # Close the connection
    return jsonify({
        "success": True,
        "message": "User added successfully"
    }), 201





if __name__ == "__main__":
    init_db()
    app.run(debug=True)