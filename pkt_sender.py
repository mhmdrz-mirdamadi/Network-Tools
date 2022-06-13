from socket import socket, AF_PACKET, SOCK_RAW
from binascii import unhexlify

message = input('What is your packet content? ')
interface = input('Which interface do you want to use? ')

sock = socket(AF_PACKET, SOCK_RAW)
sock.bind((interface, 0))
bytes_sent = sock.send(unhexlify(message))

print(f'Sent {bytes_sent}-byte packet on {interface}')
