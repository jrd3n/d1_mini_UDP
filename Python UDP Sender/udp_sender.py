# This script is so we have an easy to use udp sender for testing purposes

import socket

def send_udp_data(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode(), (ip, port))
    print("{} sent to {}:{}".format(message,ip,port))

if __name__ == "__main__":
    while True:
        send_udp_data('127.0.0.1', 1234, 'Hello, UDP server!')