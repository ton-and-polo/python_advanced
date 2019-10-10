from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_STREAM


parser = ArgumentParser()
parser.add_argument('--host', help='client address', type=str, default='127.0.0.1')
parser.add_argument('--port', help='client port', type=int, default=7777)
args = parser.parse_args()


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect((args.host, args.port))
    client.sendall('Hello, server!'.encode(encoding='utf-8'))
    data = client.recv(1024)
    print(f'message: {data.decode(encoding="utf-8")} length: {len(data)}')
