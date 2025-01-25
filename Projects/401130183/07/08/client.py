import socket

def query_dns(domain_name):
    server_address = ('127.0.0.1', 53)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    transaction_id = b'\x12\x34'
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    
    domain_parts = domain_name.split('.')
    query = b''.join([bytes([len(part)]) + part.encode() for part in domain_parts])
    query += b'\x00'
    
    request = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + b'\x00\x01\x00\x01'
    
    client_socket.sendto(request, server_address)
    
    response, _ = client_socket.recvfrom(512)
    ip_address = ".".join(map(str, response[-4:]))
    print(f"IP address of {domain_name}: {ip_address}")
    
    client_socket.close()

query_dns('google.com')
query_dns('tehran.ir')
query_dns('yahoo.com')