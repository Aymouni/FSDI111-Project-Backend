from flask import Flask, jsonify, request, render_template
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
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

# GET http://127.0.0.1:5000/api/users/2
@app.get('/api/users/<int:user_id>')
def get_user_by_id(user_id):


    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row  # Allows column values to be retrienved by name, row=["username"]
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    print(dict(row))
    user_information = dict(row)
    connection.close()

    return jsonify({
        "success": True,
        "message": "User was retrieved successfully",
        "data": user_information
    }), 200 # OK


# GET http://127.0.0.1:5000/api/users
@app.get('/api/users')
def get_users():


    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row  # Allows column values to be retrienved by name, row=["username"]
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    print(rows)
    connection.close()

    users = []
    for row in rows:
        print(dict(row))
        users.append(dict(row))

    return jsonify({
        "success": True,
        "message": "Users retrieved successfully",
        "data": users
    }), 200

# PUT http://127.0.0.1:5000/api/users/2
@app.put('/api/users/<int:user_id>')
def update_users(user_id):
    updated_user = request.get_json()
    username = updated_user["username"]
    password = updated_user["password"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # VALIDATION
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (username,password,user_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User updated successfully"
    }), 200



# DELETE http://127.0.0.1:5000/api/users/2
@app.delete('/api/users/<int:user_id>')
def delete_users(user_id):


    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # VALIDATION
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    }), 200

# ---------- EXPENSES ----------

# POST http://127.0.0.1:5000/api/expenses
@app.post('/api/expenses')
def create_expenses():
    new_expense = request.get_json()
    print(new_expense)

    title = new_expense["title"]
    description = new_expense["description"]
    amount = new_expense["amount"]
    date = new_expense["date"]
    category = new_expense["category"]
    user_id = new_expense["user_id"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses (title, description, amount, date, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)""", (title, description, amount, date, category, user_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense created successfully"
    }), 201


# GET http://127.0.0.1:5000/api/expenses
@app.get('/api/expenses')
def get_expenses():

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    print(rows)
    connection.close()

    expenses = []
    for row in rows:
        print(dict(row))
        expenses.append(dict(row))

    return jsonify({
        "success": True,
        "message": "Expenses retrieved successfully",
        "data": expenses
    }), 200


# GET http://127.0.0.1:5000/api/expenses/1
@app.get('/api/expenses/<int:expense_id>')
def get_expense(expense_id):

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    connection.close()

    if not row:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404

    print(dict(row))
    expense = dict(row)

    return jsonify({
        "success": True,
        "message": "Expense retrieved successfully",
        "data": expense
    }), 200


# PUT http://127.0.0.1:5000/api/expenses/1
@app.put('/api/expenses/<int:expense_id>')
def update_expense(expense_id):
    updated_expense = request.get_json()

    title = updated_expense["title"]
    description = updated_expense["description"]
    amount = updated_expense["amount"]
    date = updated_expense["date"]
    category = updated_expense["category"]
    user_id = updated_expense["user_id"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # VALIDATION
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404

    cursor.execute("""
        UPDATE expenses
        SET title=?, description=?, amount=?, date=?, category=?, user_id=?
        WHERE id=?
    """, (title, description, amount, date, category, user_id, expense_id))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense updated successfully"
    }), 200


# DELETE http://127.0.0.1:5000/api/expenses/1
@app.delete('/api/expenses/<int:expense_id>')
def delete_expense(expense_id):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # VALIDATION
    cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Expense deleted successfully"
    }), 200



# ---------- FRONTEND ----------
# HOME PAGE http://127.0.0.1:5000/home
@app.get('/')
@app.get('/index')
@app.get('/home')
def home():
    # logic here

    my_name = "John Doe"

    return render_template("index.html", name=my_name)

# ABOUT PAGE http://127.0.0.1:5000/about
@app.get('/about')
def about():
    info = {
        "name": "John Doe",
        "cohort": 65,
        "year": 2026
    }
    return render_template("about.html", data=info)

# CONTACT PAGE http://127.0.0.1:5000/contact
@app.get('/contact')
def contact():
    info = {
        "address": "123 Luxury Ave, San Diego, CA 92101",
        "phone": "(555) 987-6543",
        "email": "info@luxestate.com",
        "hours": "Mon - Fri: 9:00 AM - 6:00 PM"
    }
    return render_template("contact.html", data=info)



if __name__ == "__main__":
    init_db()
    app.run(debug=True)