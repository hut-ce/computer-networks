import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5050))


def stalin(array):
    print('[SORTED] Stalin sorting down')
    if not array:
        return array
    sorted_array = [array[0]]
    for i in range(1, len(array)):
        if array[i] >= sorted_array[-1]:
            sorted_array.append(array[i])
    return sorted_array


def bubble(array):
    print('[SORTED] Bubble sorting down')
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


# def bogo(array):
#     print('bogoSort')
#     def is_sorted(array):
#         return all(array[i] <= array[i + 1] for i in range(len(array) - 1))
#
#     while not is_sorted(array):
#         random.shuffle(array)
#     return array


def receiving_unsorted_msg():
    unsorted_msg = client.recv(1024).decode('utf-8')
    sort_func, str_of_numbers = unsorted_msg.split(':')
    arr_of_numbers = list(map(int, str_of_numbers.split()))

    if sort_func == 'stalin':
        msg = ' '.join(map(str, stalin(arr_of_numbers)))
        sorted_msg = ':'.join([sort_func, msg])
        client.send(sorted_msg.encode('utf-8'))

    elif sort_func == 'bubble':
        msg = ' '.join(map(str, bubble(arr_of_numbers)))
        sorted_msg = ':'.join([sort_func, msg])
        client.send(sorted_msg.encode('utf-8'))

    # elif sort_func == 'bogo':
    #     print(bogo(arr_of_numbers))

    else:
        print('sort func error')


def send_message(msg):
    client.send(num.encode('utf-8'))


try:
    while True:
        num = input("Enter your numbers(split them by using space): \n")
        if num == '0':
            receiving_unsorted_msg()
        else:
            send_message(num)
            while True:
                server_msg = client.recv(1024).decode('utf-8')
                print(server_msg)
                if not server_msg:
                    break

except KeyboardInterrupt:
    print("Connection is getting closed.")
    client.close()
