
import threading
import socket
from flask import Flask, render_template
from datetime import datetime
from lib.SQLite_DB_Tools import *

app = Flask(__name__)

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 1234))

    #SQlite Stuff
    db_file = 'my_database.db'
    conn = create_connection(db_file)
    create_table(conn)  # ensure the table is created

    while True:
        data, addr = sock.recvfrom(1024)
        print("Received message:", data, "from:", addr)

        IP = addr[0]

        handle_sensor_data(IP, data, conn)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    t = threading.Thread(target=udp_server)
    t.start()
    app.run(debug=True, host="0.0.0.0")