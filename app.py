import threading
import socket
from flask import Flask, render_template
from datetime import datetime
from lib.lmdb_Tools import *
from flask_socketio import SocketIO
# import time
import json

db_file = 'my_database.lmdb'
env = lmdb.open(db_file, map_size=1000000, max_dbs=10)
db = env.open_db(key=b'Sensor_Data')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('request_data')
def handle_request_data(last_time):
    now_time = datetime.datetime.now()
    data_dict = read_data_to_dataframe(last_time, now_time)
    # data_dict = df.to_dict(orient='records')
    json_data = json.dumps({'data': data_dict, 'timestamp': str(now_time)})

    #print(json_data)

    socketio.emit('data_response', {'data': json_data})

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 1234))
    
    while True:
        data, addr = sock.recvfrom(1024)
        IP = addr[0]

        #rint(data.decode('utf-8'))

        insert_data(env, db, datetime.datetime.now(), IP, data.decode('utf-8'))


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    t = threading.Thread(target=udp_server)
    t.start()
    socketio.run(app, debug=True, host="0.0.0.0")
    env.close()
