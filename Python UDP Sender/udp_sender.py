# This script is so we have an easy to use udp sender for testing purposes

TARGET_IP = '10.81.252.114'
TARGET_PORT = 1234

import socket

def send_udp_data(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode(), (ip, port))
    print("{} sent to {}:{}".format(message,ip,port))

if __name__ == "__main__":

    while True:
        for i in range (0,1200):
            send_udp_data(TARGET_IP, TARGET_PORT, str(i))
        for i in range (1200,0):
            send_udp_data(TARGET_IP, TARGET_PORT, str(i))
        