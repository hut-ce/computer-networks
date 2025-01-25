import socket

dns_records = {
    "google.com": "142.250.72.206",
    "facebook.com": "157.240.22.35",
    "twitter.com": "104.244.42.1",
    "github.com": "140.82.112.3",
    "youtube.com": "172.217.14.206",
    "linkedin.com": "108.174.10.10",
    "reddit.com": "151.101.1.140",
    "amazon.com": "176.32.103.205",
    "wikipedia.org": "208.80.154.224",
    "microsoft.com": "40.76.4.15"
}

def start_dns_server(host='0.0.0.0', port=53):
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_socket.bind((host, port))
    print(f"DNS Server is running on {host}:{port}")

    while True:
        data, addr = dns_socket.recvfrom(512)
        print(f"Received request from {addr}")

        query = data[12:]  
        query_name = ''
        for byte in query:
            if byte == 0:
                break
            query_name += chr(byte)

        ip_address = dns_records.get(query_name)
        
        if ip_address:
            response = b'x00x01'  
            response += b'x81x80'  
            response += b'x00x01' 
            response += b'x00x01'  
            response += data[12:]  
            response += b'xc0x0c'  
            response += b'x00x01'  
            response += b'x00x01'  
            response += b'x00x00x00x3c' 
            response += b'x00x04'  
            response += socket.inet_aton(ip_address)  

            dns_socket.sendto(response, addr)
            print(f"Sent response to {addr} with IP {ip_address}")
        else:
            print(f"No record found for {query_name}")

if __name__ == "__main__":
    start_dns_server()
