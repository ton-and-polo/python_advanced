from socket import socket, AF_INET, SOCK_STREAM

HOST = '127.0.0.1'    # All available interfaces
PORT = 7777  # Non-privileged port


with socket(AF_INET, SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    connection, address = server.accept()

    with connection:
        while True:
            data = connection.recv(1024)  # bufsize=1024B
            if not data:
                break
            print(f'message: {data.decode(encoding="utf-8")} client: {address}')
            connection.sendall('Hello, client!'.encode(encoding='utf-8'))
