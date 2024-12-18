import socket

def get_user_input():
    user_input = input("لطفا اعداد را با فاصله وارد کنید: ")
    return list(map(int, user_input.split()))

def main():
    server_address = ('localhost', 10000)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)

    try:
        numbers = get_user_input()
        s.sendall(str(numbers).encode('utf-8'))

        for _ in range(3):
            data = s.recv(1024)
            print('داده مرتب‌شده از سرور:', data.decode('utf-8'))
            s.sendall(b'ACK')  # ارسال تایید به سرور

        fastest_algo_msg = s.recv(1024)
        print(fastest_algo_msg.decode('utf-8'))
    finally:
        s.close()

if __name__ == "__main__":
    main()