from flask import Flask, render_template
import socket
import asyncio

# A simple database dictionary for storing measurements
database = {}

app = Flask(__name__)

UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 1234     # Port to listen on

def receive_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode()

        print(data)

        # # Create a JSON object with the matrix
        #json_data = json.dumps(data)
        # # print("Received message:")
        #print(json_data)

        # socketio.emit('udp_message', json_data)  # Emit UDP message to connected clients

@app.route('/')
def index():
    return render_template('index.html', measurements=database)

if __name__ == '__main__':
    import threading
    udp_thread = threading.Thread(target=receive_udp)
    udp_thread.start()
    app.run(debug=True, port=5000)