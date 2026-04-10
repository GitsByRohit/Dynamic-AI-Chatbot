from datetime import datetime
from app.db.database import get_db_connection


# -----------------------------------------
# USER QUERIES
# -----------------------------------------

def create_user(username: str, email: str, mobile: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, mobile, password)
        VALUES (?, ?, ?, ?)
    """, (username, email, mobile, password))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_by_mobile(mobile: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE mobile = ?
    """, (mobile,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# -----------------------------------------
# OTP QUERIES
# -----------------------------------------

def save_otp(identifier: str, otp: str, expires_at: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO otp_codes (identifier, otp, expires_at)
        VALUES (?, ?, ?)
    """, (identifier, otp, expires_at))

    conn.commit()
    cursor.close()
    conn.close()


def get_otp(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM otp_codes
        WHERE identifier = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (identifier,))

    otp_record = cursor.fetchone()

    cursor.close()
    conn.close()

    return otp_record


def delete_otp(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM otp_codes WHERE identifier = ?
    """, (identifier,))

    conn.commit()
    cursor.close()
    conn.close()


# -----------------------------------------
# PASSWORD UPDATE
# -----------------------------------------

def update_password(identifier: str, new_password: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE email = ? OR mobile = ?
    """, (new_password, identifier, identifier))

    conn.commit()
    cursor.close()
    conn.close()