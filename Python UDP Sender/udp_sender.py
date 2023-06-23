# This script is so we have an easy to use udp sender for testing purposes

TARGET_IP = '10.81.252.114'

import socket

def send_udp_data(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode(), (ip, port))
    print("{} sent to {}:{}".format(message,ip,port))

if __name__ == "__main__":
    while True:
        send_udp_data(TARGET_IP, 1234, '1000')
        