import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5050))
server.listen(3)
print("Server is Running...")


def stalin_sort(arr, connection):
    sorted_arr = [arr[0]]
    for item in arr[1:]:
        if item >= sorted_arr[-1]:
            sorted_arr.append(item)
        else:
            connection.send(f"'{item}' was removed from the list!\n".encode('utf-8'))
    return sorted_arr


def handle_client(connection):
    name = connection.recv(1024).decode('utf-8')

    while True:
        try:
            numbers = connection.recv(1024).decode('utf-8').split(', ')
            if not numbers:
                break
            print(f"Received data from {name}: {numbers}")

            sorted_numbers = stalin_sort(numbers, connection)
            message = f"Sorted numbers: {sorted_numbers}\n"
            print(message)
            connection.send(message.encode('utf-8'))


        except ConnectionResetError:
            print(f"{name} connections is closed.")
            break

    connection.close()
    print(f"{name} left!")


try:
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()

except KeyboardInterrupt:
    print("Server is shutting down...")
    server.close()
