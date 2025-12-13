# mysql_db.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="healthhub"
    )


# ---------------- MAIN RECORDS ----------------

def fetch_main_records():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM main_records ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_main_record(data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO main_records (label, type, description, datetime, severity)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        data["label"], data["type"], data["description"],
        data["datetime"], data["severity"]
    ))
    conn.commit()
    conn.close()


def update_main_record(record_id, data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        UPDATE main_records
        SET label=%s, type=%s, description=%s, datetime=%s, severity=%s
        WHERE id=%s
    """
    cur.execute(query, (
        data["label"], data["type"], data["description"],
        data["datetime"], data["severity"], record_id
    ))
    conn.commit()
    conn.close()


def delete_main_record(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM main_records WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()


# ---------------- WELLNESS RECORDS ----------------

def fetch_wellness_records():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM wellness_records ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_wellness_record(data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO wellness_records (label, category, frequency, description, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        data["label"], data["category"], data["frequency"],
        data["description"], data["datetime"]
    ))
    conn.commit()
    conn.close()


def update_wellness_record(record_id, data):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        UPDATE wellness_records
        SET label=%s, category=%s, frequency=%s, description=%s, datetime=%s
        WHERE id=%s
    """
    cur.execute(query, (
        data["label"], data["category"], data["frequency"],
        data["description"], data["datetime"], record_id
    ))
    conn.commit()
    conn.close()


def delete_wellness_record(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM wellness_records WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()
