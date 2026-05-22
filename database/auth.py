import bcrypt
from database.models import get_db_connection, init_database

def register_user(username, password, full_name=""):
    try:
        init_database()
        conn = get_db_connection()
        cursor = conn.cursor()

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name)
            VALUES (?, ?, ?)
        """, (username.strip().lower(), password_hash, full_name.strip()))

        conn.commit()
        conn.close()
        return True, "✅ Account created successfully!"

    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return False, "❌ Username already exists. Choose another."
        return False, f"❌ Error: {str(e)}"


def login_user(username, password):
    try:
        init_database()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip().lower(),))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return False, None, "❌ Username not found."

        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return True, dict(user), "✅ Login successful!"
        else:
            return False, None, "❌ Wrong password."

    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None