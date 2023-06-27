import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'successful SQLite connection with sqlite version {sqlite3.version}')
        return conn
    except Error as e:
        print(f"Error {e.args[0]}: {e}")

def close_connection(conn):
    conn.close()
    print('SQLite connection is closed')

def create_table(conn):

    try:
        query = '''CREATE TABLE IF NOT EXISTS Sensor_Data (
                        id INTEGER PRIMARY KEY,
                        event_time TEXT NOT NULL,
                        ip_address TEXT,
                        Raw_value REAL);'''
        conn.execute(query)
    except Error as e:
        print(e)

def insert_data(conn, event_time, ip_address, Raw_value):

    try:
        query = '''INSERT INTO Sensor_Data(event_time, ip_address, Raw_value) 
                VALUES(?, ?, ?);'''
        conn.execute(query, (event_time, ip_address, Raw_value))
        conn.commit()
    except Error as e:
        print(e)

def read_all_data(conn):

    try:
        query = '''SELECT * FROM Sensor_Data;'''
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(e)

def read_data_to_dataframe(conn,start_time = "all", end_time = "all"):

    start_time = '2023-06-01 00:00:00'  # Specify the start time
    end_time = '2023-07-02 00:00:00'  # Specify the end time

    query = f"SELECT * FROM Sensor_Data WHERE event_time BETWEEN '{start_time}' AND '{end_time}';"
    df = pd.read_sql_query(query, conn)
    
    # Check if 'ip_address' column exists in the DataFrame
    if 'ip_address' not in df.columns:
        print("Error: 'ip_address' column not found in the DataFrame.")
        return None

    # Replace value with Raw_value for each unique IP address
    unique_ips = df['ip_address'].unique()
    for ip in unique_ips:
        mask = df['ip_address'] == ip
        df.loc[mask, ip] = df.loc[mask, 'Raw_value']

        # Filter and remove rows where the value is the same as the previous row
        df[df[ip].diff()!=0]

    # Assuming your DataFrame is named 'df'
    df['event_time'] = pd.to_datetime(df['event_time'], format='%Y-%m-%d %H:%M:%S.%f')

    # Set 'event_time' as the index
    df.set_index('event_time', inplace=True)

    df.drop(['id','ip_address','Raw_value'], axis=1, inplace=True)

    # print(df)

    shrunken_df = df.resample('1S').mean()

    # print(shrunken_df)
    
    # Calculate the mean of 100 readings using rolling window
    #df['rolling_mean'] = df['value'].rolling(window=100).mean()
    
    return shrunken_df

def plot_data(df):
    # Assuming your DataFrame is named 'df'
    df.plot(y='10.81.252.114', legend=False)
    plt.xlabel('Event Time')
    plt.ylabel('Value')
    plt.title('Plot of 10.81.252.114')
    plt.show()

if __name__ == "__main__":
    db_file = 'my_database.db'
    conn = create_connection(db_file)

    df = read_data_to_dataframe(conn)
    plot_data(df)

    close_connection(conn)