from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from pymongo import MongoClient

app = Flask(__name__)

# ==========================================
# הגדרות חיבור למסדי הנתונים
# ==========================================

# חיבור ל-SQL Server באמצעות Named Pipes מקומי
SQL_SERVER = 'np:localhost'
SQL_DATABASE = 'fullstack_db'

sql_connection_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"Trusted_Connection=yes;"
    f"Encrypt=no;"
)

# חיבור ל-MongoDB עבור לוגים של פעילות משתמשים
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['fullstack_logs_db']
logs_collection = mongo_db['user_activity_logs']


# ==========================================
# Routes / ניתובים של האפליקציה
# ==========================================

@app.route('/')
def index():
    """דף הבית: שולף משתמשים מ-SQL Server ואת הלוגים האחרונים מ-MongoDB"""

    # שליפת משתמשים מ-SQL Server
    users = []
    try:
        conn = pyodbc.connect(sql_connection_str)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM users')
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"SQL Server error: {e}")

    # שליפת לוגים מ-MongoDB
    logs = []
    try:
        logs = list(logs_collection.find().sort('_id', -1).limit(5))
    except Exception as e:
        print(f"MONGO error: {e}")

    return render_template('index.html', users=users, logs=logs)


@app.route('/add', methods=['POST'])
def add_user():
    """הוספת משתמש חדש ל-SQL Server ותיעוד הפעולה כלוג ב-MongoDB"""
    name = request.form.get('name')
    email = request.form.get('email')

    if name and email:
        # שמירה ב-SQL Server
        try:
            conn = pyodbc.connect(sql_connection_str)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving to SQL SERVER: {e}")

        # שמירת לוג ב-MongoDB
        try:
            log_entry = {
                "action": "USER_CREATED",
                "user_name": name,
                "email": email,
            }
            logs_collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")

    return redirect(url_for('index'))


@app.route('/delete-all', methods=['POST'])
def delete_all_users():
    """מחיקת כל המשתמשים מ-SQL Server ואיפוס מונה ה-ID"""
    try:
        conn = pyodbc.connect(sql_connection_str)
        cursor = conn.cursor()
        cursor.execute('TRUNCATE TABLE users')
        conn.commit()
        conn.close()
        print("All users deleted and IDs reset successfully!")
    except Exception as e:
        print(f"Error deleting users from SQL Server: {e}")

    return redirect(url_for('index'))


@app.route('/delete-all-logs', methods=['POST'])
def delete_all_logs():
    """מחיקת כל הלוגים מקולקציית MongoDB"""
    try:
        result = logs_collection.delete_many({})
        print(f"Deleted {result.deleted_count} logs successfully from MongoDB!")
    except Exception as e:
        print(f"Error clearing logs from MongoDB: {e}")

    return redirect(url_for('index'))


# ==========================================
# הפעלת השרת
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)