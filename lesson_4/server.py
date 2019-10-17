import json
from socket import socket, AF_INET, SOCK_STREAM
from configs import (
    HOST,
    PORT,
    MAX_CONNECTIONS,
    BUF_SIZE,
    ENCODING,
    ACTION,
    TIME,
    USER,
    PRESENCE,
    ACCOUNT_NAME,
    RESPONSE,
)


def get_message(connection):
    data = connection.recv(BUF_SIZE)
    if data:
        data.decode(ENCODING)
        return json.loads(data)


def process(message: dict):
    if all(required_key in message.keys() for required_key in [ACTION, TIME, USER]):
        if message[ACTION] == PRESENCE and message[USER][ACCOUNT_NAME] == 'guest':
            return {RESPONSE: 200}
    return {RESPONSE: 400}


def send_message(connection, message):
    message = json.dumps(message)
    connection.send(message.encode(ENCODING))


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(MAX_CONNECTIONS)

        connection, address = server.accept()
        with connection:
            print(f'connected by: {address}', end=' ')
            while True:
                message = get_message(connection)
                if message:
                    print(f'data: {message}')
                    send_message(connection, process(message))
                else:
                    break
