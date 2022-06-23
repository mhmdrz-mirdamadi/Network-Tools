from socket import inet_aton
from tcp_syn_sender import syn_sender

if __name__ == '__main__':
    dest_ip = input('What is the target IP address? ')
    ports = input('Which ports do you want to scan? ')
    ports = list(map(int, ports.split('-')))
    for port in range(ports[0], ports[1]):
        if syn_sender(destination_IP=inet_aton(dest_ip).hex(),
                      destination_port='%04x' % int(port)):
            print(f'Sent TCP SYN packet to port {port}')
