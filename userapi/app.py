import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', '127.0.0.1')  # Default to 127.0.0.1 for local testing
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'my-secret-pw')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops_userdb')
app.secret_key = 'super_secret_key' # Required for sessions/flash messages (good practice)

mysql = MySQL(app)
# --- End Configuration ---

# -----------------
# 1. CREATE User (POST)
# -----------------
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    # NOTE: In a real app, hash the password (e.g., using bcrypt)
    password = data['password']

    cursor = mysql.connection.cursor()
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'User with this email already exists'}), 409
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        mysql.connection.commit()
        return jsonify({'message': 'User created successfully', 'name': name}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500
    finally:
        cursor.close()

# -----------------
# 2. READ All Users (GET)
# -----------------
@app.route('/users', methods=['GET'])
def get_all_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # Get results as dictionaries
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    
    # Check if users is empty (for health check/testing)
    if users:
        return jsonify(users), 200
    else:
        return jsonify({'message': 'No users found'}), 404

# -----------------
# 3. UPDATE User (PUT) - by ID
# -----------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password') # Only update if provided

    cursor = mysql.connection.cursor()
    # Build the query dynamically based on provided fields
    updates = []
    params = []
    
    if name:
        updates.append("name = %s")
        params.append(name)
    if email:
        updates.append("email = %s")
        params.append(email)
    if password:
        # NOTE: In a real app, hash the password before update
        updates.append("password = %s")
        params.append(password)
        
    if not updates:
        return jsonify({'message': 'No fields provided for update'}), 400

    # Final query construction
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
# 5. HEALTH CHECK (GET) - Required for the project
# -----------------
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Attempt to get a connection and execute a simple query (e.g., SELECT 1)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return jsonify({'status': 'UP', 'database_connection': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'DOWN', 'database_connection': 'FAILED', 'error': str(e)}), 503

if __name__ == '__main__':
    # Use 0.0.0.0 for containerized/VM deployment compatibility
    app.run(debug=True, host='0.0.0.0', port=5000)