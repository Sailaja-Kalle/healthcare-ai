from database.models import get_db_connection, init_database

def save_history(user_id, tab_type, query, response, language="English"):
    try:
        init_database()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chat_history (user_id, tab_type, query, response, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, tab_type, query, response, language))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"History save error: {e}")
        return False


def get_user_history(user_id, tab_type=None, limit=50):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if tab_type:
            cursor.execute("""
                SELECT * FROM chat_history
                WHERE user_id = ? AND tab_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, tab_type, limit))
        else:
            cursor.execute("""
                SELECT * FROM chat_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    except Exception as e:
        print(f"History fetch error: {e}")
        return []


def delete_user_history(user_id, history_id=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if history_id:
            cursor.execute("""
                DELETE FROM chat_history
                WHERE id = ? AND user_id = ?
            """, (history_id, user_id))
        else:
            cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"History delete error: {e}")
        return False


def get_history_stats(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tab_type, COUNT(*) as count
            FROM chat_history
            WHERE user_id = ?
            GROUP BY tab_type
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()
        return {row['tab_type']: row['count'] for row in rows}

    except Exception as e:
        print(f"Stats error: {e}")
        return {}