import csv
import threading
import socket
from flask import Flask, render_template
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

data_dict = defaultdict(str)  # Will store IPs as keys and most recent data as values
fieldnames = ["Time"]  # List of fieldnames for the CSV, starting with "Time"

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 1234))

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("Received message:", data, "from:", addr)

        ip = addr[0]
        if ip not in fieldnames:
            fieldnames.append(ip)  # If IP is new, add it to the fieldnames

        for key in data_dict:  # Reset the dict for new row
            data_dict[key] = ''
        
        data_dict[ip] = data  # Store most recent data

        # Append the new row to the CSV
        append_csv()

def append_csv():
    with open('udp_data.csv', 'a', newline='') as file:  # Open the file in append mode
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # Check if the file is empty
            writer.writeheader()  # If it is, write the headers
        writer.writerow({"Time": datetime.now().isoformat(), **data_dict})


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
        # Write the CSV headers when the program starts
    with open('udp_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    t = threading.Thread(target=udp_server)
    t.start()
    app.run(debug=True)