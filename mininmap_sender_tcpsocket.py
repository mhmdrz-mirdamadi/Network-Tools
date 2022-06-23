from socket import socket, AF_INET, SOCK_STREAM
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='args')
    parser.add_argument('-t', default=1, type=int,
                        help='Timeout for TCP connection in milliseconds')
    args = parser.parse_args()

    dest_ip = input('What is the target IP address? ')
    ports = input('Which ports do you want to scan? ')
    ports = list(map(int, ports.split('-')))
    for port in range(ports[0], ports[1]):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(args.t / 1000)
            sock.connect((dest_ip, port))
        except:
            sock.close()
