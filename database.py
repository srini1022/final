import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'finalproject',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def query_db(query, args=(), fetchone=False, commit=False):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            if commit:
                conn.commit()
                return cursor.lastrowid
            
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall()
    finally:
        conn.close()
