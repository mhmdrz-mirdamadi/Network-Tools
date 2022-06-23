from socket import socket, AF_PACKET, SOCK_RAW
from binascii import unhexlify


def sender(message, interface):
    sock = socket(AF_PACKET, SOCK_RAW)
    sock.bind((interface, 0))
    bytes_sent = sock.send(unhexlify(message))
    return bytes_sent


if __name__ == '__main__':
    message = input('What is your packet content? ')
    interface = input('Which interface do you want to use? ')
    print(f'Sent {sender(message, interface)}-byte packet on {interface}')
