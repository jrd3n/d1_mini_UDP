import sqlite3
from sqlite3 import Error
import datetime
import pandas as pd

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'successful SQLite connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(f"Error {e.args[0]}: {e}")
    return conn

def close_connection(conn):
    conn.close()
    print('SQLite connection is closed')

def create_table(conn):
    try:
        query = '''CREATE TABLE IF NOT EXISTS time_series_data (
                        id INTEGER PRIMARY KEY,
                        event_time TEXT NOT NULL,
                        value REAL,
                        extra_column TEXT);'''
        conn.execute(query)
    except Error as e:
        print(e)

def insert_data(conn, event_time, value, extra_data):
    try:
        query = '''INSERT INTO time_series_data(event_time, value, extra_column) 
                   VALUES(?, ?, ?);'''
        conn.execute(query, (event_time, value, extra_data))
        conn.commit()
    except Error as e:
        print(e)

def read_all_data(conn):
    try:
        query = '''SELECT * FROM time_series_data;'''
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(e)

def handle_sensor_data(ip_address, value, conn):
    event_time = datetime.datetime.now().isoformat()
    insert_data(conn, event_time, value, ip_address)

def read_data_to_dataframe(conn):
    query = '''SELECT * FROM time_series_data;'''
    df = pd.read_sql_query(query, conn)
    return df

if __name__ == "__main__":
    db_file = 'my_database.db'
    conn = create_connection(db_file)


    handle_sensor_data('192.168.1.205', '1234', conn)

    # read_all_data(conn)

    df = read_data_to_dataframe(conn)
    print(df)

    close_connection(conn)
