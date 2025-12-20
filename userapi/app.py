import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'my-secret-pw')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops_userdb')
app.secret_key = 'super_secret_key'

mysql = MySQL(app)
# --- End Configuration ---

# Create table on startup
def init_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(100) NOT NULL,
              email VARCHAR(100) UNIQUE NOT NULL,
              password VARCHAR(255) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        cursor.close()
        print("✓ Users table initialized")
    except Exception as e:
        print(f"✗ Database init failed: {e}")

with app.app_context():
    init_db()

# -----------------
# 1. CREATE User (POST)
# -----------------
@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        # These will raise KeyError if missing
        name = data['name']
        email = data['email']
        password = data['password']

        # Only connect to DB AFTER validation
        cursor = mysql.connection.cursor()

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({'message': 'User with this email already exists'}), 409
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User created successfully', 'name': name}), 201

    except Exception as e:
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500
        
# -----------------
# 2. READ All Users (GET)
# -----------------
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()

        if not users:
            return jsonify({"message": "No users found"}), 200

        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": "Database unavailable"}), 503

# -----------------
# 3. UPDATE User (PUT) - by ID
# -----------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    updates = []
    params = []
    
    if name:
        updates.append("name = %s")
        params.append(name)
    if email:
        updates.append("email = %s")
        params.append(email)
    if password:
        updates.append("password = %s")
        params.append(password)
        
    if not updates:
        return jsonify({'message': 'No fields provided for update'}), 400

    query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = %s"
    params.append(user_id)

    try:
        cursor.execute(query, tuple(params))
        mysql.connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'message': f'User with ID {user_id} not found'}), 404
        
        return jsonify({'message': f'User ID {user_id} updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error updating user', 'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------
# 4. DELETE User (DELETE) - by ID
# -----------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'message': f'User with ID {user_id} not found'}), 404
            
        return jsonify({'message': f'User ID {user_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error deleting user', 'error': str(e)}), 500
    finally:
        cursor.close()


# -----------------
# 5. HEALTH CHECK (GET)
# -----------------
@app.route('/health', methods=['GET'])
def health_check():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return jsonify({'status': 'UP', 'database_connection': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'DOWN', 'database_connection': 'FAILED', 'error': str(e)}), 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)