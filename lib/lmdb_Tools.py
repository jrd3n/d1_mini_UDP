import lmdb
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from pandas import json_normalize
import json
import datetime
import time

# Open or create the LMDB database
db_file = 'my_database.lmdb'
env = lmdb.open(db_file, map_size=1000000, max_dbs=10)
db = env.open_db(key=b'Sensor_Data')

def insert_data(env, db, event_time, ip_address, Raw_value):
    data = {
        'event_time': event_time,
        'ip_address': ip_address,
        'Raw_value': Raw_value,
    }
    pickled_data = pickle.dumps(data)  # Ensure data is pickled before being stored
    with env.begin(write=True) as txn:
        key = str(int(time.mktime(event_time.timetuple()))).encode() # Convert event_time to timestamp and use it as key
        txn.put(key, pickled_data, db=db)

def read_all_data():
    data = []
    with env.begin() as txn: 
        cursor = txn.cursor(db)
        for key, value in cursor:
            data.append(pickle.loads(value))  # use pickle.loads instead of json.loads
    df = pd.DataFrame(data)  # Convert list to DataFrame
    df['event_time'] = pd.to_datetime(df['event_time'])  # Ensure event_time is datetime type
    df['Raw_value'] = pd.to_numeric(df['Raw_value'], errors='coerce')
    df.set_index('event_time', inplace=True)
    return df

def df_to_json(df):
    json_data = df.reset_index().groupby('ip_address')[['event_time', 'Raw_value']].apply(lambda x: x.to_dict('records')).reset_index().rename(columns={0:'data'}).to_json(orient='records')
    return json_data


def read_data_to_dataframe(start_time=None, end_time=None):
    df = read_all_data()

    # Convert your dataframe index to datetime and sort it
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # print("Min {} -- Max {}".format(start_time,end_time))
    # print("Min {} -- Max {}".format(df.index.min(),df.index.max()))

    if start_time == None or start_time == 0:
        start_time = df.index.min()
        # print(start_time)

    if end_time == None or end_time > df.index.max():
        end_time = df.index.max()
        # print(end_time)

    df = df.loc[start_time:end_time]

    return df_to_json(df)


def plot_data(df):
    df.plot(y='Raw_value', legend=False)  # Plot Raw_value, not ip_address
    plt.xlabel('Event Time')
    plt.ylabel('Value')
    plt.title('Plot of ip_address')
    plt.show()

if __name__ == "__main__":
    end_time = datetime.datetime.now()  # end_time as datetime object
    df = read_data_to_dataframe(start_time=None, end_time=end_time)
    print(df)
    plot_data(df)
    env.close()
