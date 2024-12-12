import socket
import threading
import logging


logging.basicConfig(filename='server.log',level=logging.INFO)


def broadcast(data, clients):
    for client in clients:
        try:
            client.send(data.encode())
        except Exception as e:
            logging.error(f'Error sending data to a client: {e}')

def handle_client(client, clients, results):
    try:
        
        data = client.recv(1024).decode('utf-8')
        if ',' in data:
            algorithm, time, sorted_array = data.split(',')
            results[algorithm] = {'time': float(time), 'sorted_array': sorted_array}
            logging.info(f"Received result for {algorithm} - spent time is {time}")

            if len(results) == 3:
                fastest_algorithm = None
                fastest_time = float('inf')
                for alg, result in results.items():
                    if result['time'] < fastest_time: 
                        fastest_time = result['time'] 
                        fastest_algorithm = [alg] 
                    elif result['time'] == fastest_time: 
                        fastest_algorithm.append(alg)
                        
                if len(fastest_algorithm) == 1:
                    logging.info(f"The fastest algorithm is: {fastest_algorithm[0]}")
                else:
                    logging.info(f"The fastest algorithms are: {', '.join(fastest_algorithm)}")
                
                for alg, result in results.items():
                    #print(result)
                    logging.info(f"Algorithm: {alg}, Sorted Array: {result['sorted_array']}")
        else:
            array = list(map(int, data.split()))
            logging.info(f"Received array: {array}")

            
            broadcast(data, clients)
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client.close()

def start_server(server):
    try:
        

        clients = []
        results = {}

        while True:
            client, addr = server.accept()
            logging.info(f'Connected by {addr}')
            clients.append(client)

            if len(clients) == 4:
                for client in clients:
                    thread = threading.Thread(target=handle_client, args=(client, clients, results))
                    thread.start()
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5050))
    server.listen(4)
    logging.info('Server is listening...')
    start_server(server)

if __name__ == '__main__':
    main()
