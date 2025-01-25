import socket
import struct
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

ip_pool = [f"192.168.1.{i}" for i in range(100, 200)]
leased_ips = {}


def send_packet(sock, addr, data):
    sock.sendto(data, addr)


def receive_packet(sock):
    data, addr = sock.recvfrom(1024)
    return data, addr


def handle_dhcp_discovery(sock, addr, xid):
    offer_ip = random.choice(ip_pool)
    leased_ips[addr[0]] = offer_ip
    offer_packet = struct.pack('!4sI4s', b'\x02', xid, socket.inet_aton(offer_ip))
    send_packet(sock, addr, offer_packet)


def handle_dhcp_request(sock, addr, xid):
    ack_packet = struct.pack('!4sI4s', b'\x05', xid, socket.inet_aton(leased_ips[addr[0]]))
    send_packet(sock, addr, ack_packet)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print("Server is Running and is waiting for connections...")

    while True:
        data, addr = receive_packet(server_socket)
        msg_type, xid, _ = struct.unpack('!4sI4s', data[:12])

        if msg_type == b'\x01':
            handle_dhcp_discovery(server_socket, addr, xid)
        elif msg_type == b'\x03':
            handle_dhcp_request(server_socket, addr, xid)


if __name__ == '__main__':
    main()
