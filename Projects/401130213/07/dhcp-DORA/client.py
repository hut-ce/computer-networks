import socket
import struct
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050


def send_packet(sock, addr, data):
    sock.sendto(data, addr)


def receive_packet(sock):
    data, addr = sock.recvfrom(1024)
    return data, addr


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((IP, PORT))

    xid = random.randint(1, 100000)
    discover_packet = struct.pack('!4sI4s', b'\x01', xid, b'\x00' * 4)
    send_packet(client_socket, ('255.255.255.255', 67), discover_packet)
    print("Sent DHCPDISCOVER")

    data, _ = receive_packet(client_socket)
    msg_type, server_xid, offered_ip = struct.unpack('!4sI4s', data[:12])
    if msg_type == b'\x02' and server_xid == xid:
        print(f"Received DHCPOFFER: {socket.inet_ntoa(offered_ip)}")

        request_packet = struct.pack('!4sI4s', b'\x03', xid, offered_ip)
        send_packet(client_socket, ('255.255.255.255', 67), request_packet)
        print("Sent DHCPREQUEST")

        data, _ = receive_packet(client_socket)
        msg_type, server_xid, ack_ip = struct.unpack('!4sI4s', data[:12])
        if msg_type == b'\x05' and server_xid == xid:
            print(f"Received DHCPACK: {socket.inet_ntoa(ack_ip)}")


if __name__ == '__main__':
    main()
