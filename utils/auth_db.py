import os
import sqlite3
import hashlib
import datetime
import pandas as pd

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "app_data.db")

def init_db():
    """Initializes SQLite database and tables if they do not exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # File Analysis Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        size_mb REAL NOT NULL,
        sha256_hash TEXT NOT NULL,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def hash_password(password):
    """Generates SHA-256 salted hash of password."""
    salt = "SmartFileAnalyzerSalt2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def register_user(username, email, password):
    """Registers a new user into the database."""
    init_db()
    if not username or not email or not password:
        return False, "All fields are required."

    p_hash = hash_password(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username.strip(), email.strip().lower(), p_hash)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists. Please choose another."
    except Exception as e:
        return False, f"Database error: {e}"

def verify_user(username, password):
    """Verifies user login credentials."""
    init_db()
    p_hash = hash_password(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (username.strip(), p_hash)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return True, {"id": row[0], "username": row[1], "email": row[2]}
        return False, "Invalid username or password."
    except Exception as e:
        return False, f"Database error: {e}"

def log_file_analysis(username, df_files):
    """Stores analyzed file records into database history log."""
    if df_files is None or df_files.empty:
        return

    init_db()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for _, row in df_files.iterrows():
            cursor.execute(
                """
                INSERT INTO analysis_logs (username, filename, file_type, size_mb, sha256_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    username,
                    row.get("File Name", "Unknown"),
                    row.get("Type", "Other"),
                    float(row.get("Size (MB)", 0.0)),
                    row.get("SHA-256", "N/A")
                )
            )
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_user_history(username):
    """Fetches past file analysis history for logged-in user."""
    init_db()
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT filename, file_type, size_mb, sha256_hash, analyzed_at FROM analysis_logs WHERE username = ? ORDER BY id DESC LIMIT 50"
        df = pd.read_sql_query(query, conn, params=(username,))
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()
