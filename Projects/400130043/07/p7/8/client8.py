import socket

def dns_query(domain, server_ip='127.0.0.1'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    request = b'x00x01'  
    request += b'x01x00'  
    request += b'x00x01'  
    request += b'x00x00'  
    request += b'x00x00'  
    request += b'x00x00'  

    for part in domain.split('.'):
        request += bytes([len(part)]) + part.encode('utf-8')
    request += b'x00'  

    request += b'x00x01'  
    request += b'x00x01'  

    sock.sendto(request, (server_ip, 53))

    response, _ = sock.recvfrom(512)

    ip_address = socket.inet_ntoa(response[-4:])
    
    return ip_address

if __name__ == "__main__":
    domain = input("Enter the domain you want to query: ")
    
    server_ip = input("Enter the DNS server IP (default is 127.0.0.1): ") or '127.0.0.1'
    
    ip_address = dns_query(domain, server_ip)
    
    print(f"The IP address for {domain} is {ip_address}")
