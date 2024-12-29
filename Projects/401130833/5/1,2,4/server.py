import socket
import threading
import time

class SortingServer:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(10)
        self.clients = []
        self.sorting_algorithms = {
            1: "Stalin Sort",
            2: "Bogo Sort",
            3: "Bubble Sort"
        }

    def broadcast_sort_request(self, array, source_client):
        threads = []
        results = {}
        for i, client in enumerate(self.clients):
            if client == source_client:
                continue
            algo_id = (i % 3) + 1
            thread = threading.Thread(
                target=self.send_sort_request,
                args=(client, algo_id, array, results),
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return results

    def send_sort_request(self, client, algo_id, array, results):
        try:
            client.send(f"answer|{algo_id}|{','.join(map(str, array))}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            results[algo_id] = list(map(int, response.split(',')))
        except (ConnectionResetError, ConnectionAbortedError):
            print("A client disconnected during sorting.")

    def handle_client(self, connection, address):
        print(f"Client {address} connected.")
        self.clients.append(connection)
        try:
            while True:
                command = connection.recv(1024).decode()
                if command.startswith("sort|"):
                    array = list(map(int, command.split("|")[1].split(",")))
                    print(f"Received array from {address}: {array}")
                    results = self.broadcast_sort_request(array, connection)
                    connection.send(
                        f"sorted|{','.join(map(str, results.values()))}".encode('utf-8')
                    )
        except (ConnectionResetError, KeyboardInterrupt):
            print(f"Connection with {address} closed.")
        finally:
            self.clients.remove(connection)
            connection.close()

    def start(self):
        print("Server is running...")
        try:
            while True:
                connection, address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(connection, address)).start()
        except KeyboardInterrupt:
            print("Shutting down server...")
            self.server.close()

if __name__ == "__main__":
    server = SortingServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()
