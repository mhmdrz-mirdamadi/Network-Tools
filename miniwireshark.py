from socket import socket, AF_PACKET, SOCK_RAW, ntohs, inet_ntoa
from struct import unpack


def unpack_link_layer(data):
    dest_mac, src_mac, prototype = unpack('! 6s 6s 2s', data[0:14])
    return {'dest_mac': dest_mac.hex(),
            'src_mac': src_mac.hex(),
            'prototype': prototype.hex()}, data[14:]


def unpack_network_layer(data):
    data_copy = data
    data = unpack('! B s H 2s 2s B B 2s 4s 4s', data[:20])
    version = data[0] >> 4
    length = (data[0] & 0x0F) * 4
    diffserv = data[1].hex()
    total_length = data[2]
    id = data[3].hex()
    flags = data[4].hex()
    ttl = data[5]
    protocol = data[6]
    checksum = data[7].hex()
    src_ip = inet_ntoa(data[8])
    dest_ip = inet_ntoa(data[9])

    return {'version': version,
            'length': length,
            'diffserv': diffserv,
            'total_length': total_length,
            'id': id,
            'flags': flags,
            'ttl': ttl,
            'protocol': protocol,
            'checksum_ip': checksum,
            'src_ip': src_ip,
            'dest_ip': dest_ip}, data_copy[length:]


def unpack_tcp(data):
    data = unpack('! H H I I H H 2s 2s', data[:20])
    src_port = data[0]
    dest_port = data[1]
    seq_num = data[2]
    ack_num = data[3]
    offset = data[4] >> 12
    flags = data[4] & 0xFFF
    window_size = data[5]
    checksum_tcp = data[6].hex()
    urgent_pointer = data[7].hex()

    return {'src_port': src_port,
            'dest_port': dest_port,
            'seq_num': seq_num,
            'ack_num': ack_num,
            'offset': offset,
            'flags': flags,
            'window_size': window_size,
            'checksum_tcp': checksum_tcp,
            'urgent_pointer': urgent_pointer}, data[20:]


if __name__ == '__main__':
    conn = socket(AF_PACKET, SOCK_RAW, ntohs(0x0003))
    while True:
        raw_data, _ = conn.recvfrom(65535)
        info_link, network = unpack_link_layer(raw_data)
        info_network, transport = unpack_network_layer(network)
        if info_network['protocol'] == 6:  # is tcp?
            info_tcp, _ = unpack_tcp(transport)
            if info_tcp['flags'] & 0b010010 == 0b010010:  # is syn-ack?
                print(
                    f"Port {info_tcp['src_port']} is open on {info_network['src_ip']}")
