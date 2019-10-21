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
import logging
import logs.configs.server_log_config


# Create a logger:
logger = logging.getLogger('server_logger')


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
        logger.info(f'Start server at {HOST}:{PORT}')
        server.listen(MAX_CONNECTIONS)

        connection, address = server.accept()
        with connection:
            logger.info(f'Connected by: {address}')
            while True:
                message = get_message(connection)
                if message:
                    logger.info(f'Connection {address} data: {message}')
                    send_message(connection, process(message))
                else:
                    break
