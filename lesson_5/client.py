import json
import time
from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_STREAM
from configs import (
    HOST,
    PORT,
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
import logs.configs.client_log_config


logger = logging.getLogger('client_logger')

parser = ArgumentParser()
parser.add_argument('--host', help='client address', type=str, default=HOST)
parser.add_argument('--port', help='client port', type=int, default=PORT)
args = parser.parse_args()

if 65535 < args.port < 1033:
    logger.error('Invalid port')
    raise parser.error('Invalid port')


def presence_message():
    status = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
        USER: {ACCOUNT_NAME: 'guest'}
    }
    return status


def process(message: dict):
    if message[RESPONSE]:
        return message[RESPONSE]


def send_message(connection, message):
    message = json.dumps(message)
    connection.send(message.encode(ENCODING))


def get_message(connection):
    data = connection.recv(BUF_SIZE)
    if data:
        data.decode(ENCODING)
        return json.loads(data)


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((args.host, args.port))
        logger.info(f'Connected to server at {args.host}:{args.port}')

        client_message = presence_message()
        send_message(client, client_message)
        logger.info(f'Send {client_message} to server')
        data = process(get_message(client))
        if data:
            logger.info(f'Received data: {data} from server')
