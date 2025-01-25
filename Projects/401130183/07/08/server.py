import socket

dns_records = {
    "google.com": "142.250.190.14",
    "yahoo.com": "98.137.246.8",
    "tehran.ir": "185.14.232.10",
    "irna.ir": "185.2.122.5",
    "digikala.com": "185.85.0.10",
    "t.me": "185.17.224.139",
    "namnak.com": "185.54.199.10",
    "shahrekhabar.com": "185.129.100.10",
    "tap30.ir": "185.173.93.10",
    "snapp.ir": "185.128.129.7"
}

def handle_dns_request(data, addr, server_socket):
    domain_name = data[12:].decode('utf-8').split("\x00")[0]
    if domain_name in dns_records:
        ip_address = dns_records[domain_name]
        response = create_dns_response(data, ip_address)
        server_socket.sendto(response, addr)
    else:
        server_socket.sendto(b"Domain not found", addr)

def create_dns_response(request, ip_address):
    transaction_id = request[:2]
    flags = b"\x81\x80"
    questions = b"\x00\x01"
    answer_rrs = b"\x00\x01"
    authority_rrs = b"\x00\x00"
    additional_rrs = b"\x00\x00"
    
    query = request[12:]
    response_header = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs
    
    response_body = query + b"\x00\x01\x00\x01\x00\x00\x00\x00\x00\x04" + bytes(map(int, ip_address.split('.')))
    
    return response_header + response_body

def start_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 53))
    while True:
        data, addr = server_socket.recvfrom(512)
        handle_dns_request(data, addr, server_socket)

start_dns_server()
