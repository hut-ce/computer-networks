import socket

# Main client function
def main():
    host = '127.0.0.1'
    port = 65432

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print("Connected to the server.")

            # Input array from user
            array = list(map(int, input("Enter numbers separated by space: ").split()))

            # Send array to the server as a comma-separated string
            client_socket.send(",".join(map(str, array)).encode())

            # Receive the response from the server
            response = client_socket.recv(4096).decode()

            if response.startswith("Error:"):
                print(f"Server Error: {response}")
            else:
                print("\nSorting Results:")
                results = response.split(";")
                for result in results:
                    algo_name, sorted_array, duration = result.split(":")
                    print(f"Algorithm: {algo_name}, Time: {duration}s, Sorted Array: {sorted_array}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
