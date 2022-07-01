from socket import inet_aton
from checksum import cs
from pkt_sender import sender

lines: list
with open('info.txt', 'r') as fd:
    lines = fd.readlines()

interface = lines[4][:-1]

dest_mac = lines[6][:17]  # destination MAC address
src_mac = lines[5][:17]  # source MAC address
proto3 = '08 00'  # layer 3 protocol number

ver_ihl = '45'  # version, header length
tos = '00'  # type-of-service
total_len = '00 28'  # total length -> 40 bytes
id = '07 c3'  # ID
flags = '40 00'  # flags and fragment offset
ttl = '40'  # time-to-live
proto4 = '06'  # layaer 4 protocol num
src_ip = inet_aton(lines[2]).hex()  # source IP address
dest_ip = inet_aton(lines[0]).hex()  # destination IP address

src_port = '%04x' % int(lines[3])  # source port
dest_port = '%04x' % int(lines[1])  # destination port
seq_num = '17 49 30 d1'  # sequence number
ack = '00 00 00 00'  # acknowledgement number
tcp_hl = '50 02'  # TCP header length and flags
win_size = '72 10'  # window size
up = '00 00'  # urgent pointer


def frame_calc(destination_MAC=dest_mac,
               source_MAC=src_mac,
               protocol=proto3):
    # Ethernet Frame
    return (destination_MAC + source_MAC +
            protocol).replace(' ', '')


def datagram_calc(version_headerlength=ver_ihl,
                  TOS=tos,
                  total_length=total_len,
                  ID=id,
                  flags_fragmentation_offset=flags,
                  TTL=ttl,
                  protocol=proto4,
                  source_IP=src_ip,
                  destination_IP=dest_ip):
    # IP Datagram
    datagram_cs = (version_headerlength + TOS + total_length +
                   ID + flags_fragmentation_offset + TTL +
                   protocol + '00 00' + source_IP +
                   destination_IP).replace(' ', '')
    datagram_cs = ' '.join(datagram_cs[i:i + 2]
                           for i in range(0, len(datagram_cs), 2))
    checksum_calculated = cs(datagram_cs)
    return(version_headerlength + TOS + total_length + ID +
           flags_fragmentation_offset + TTL + protocol +
           checksum_calculated + source_IP + destination_IP
           ).replace(' ', '')


def segment_calc(source_IP=src_ip,
                 destination_IP=dest_ip,
                 protocol=proto4,
                 source_port=src_port,
                 destination_port=dest_port,
                 sequence_number=seq_num,
                 acknowledgement_number=ack,
                 TCP_headerlength=tcp_hl,
                 window_size=win_size,
                 urgent_pointer=up):
    # TCP Segments
    pseudo_header = source_IP + destination_IP + '00' + protocol + '00 14'
    segment_cs = (pseudo_header + source_port + destination_port +
                  sequence_number + acknowledgement_number +
                  TCP_headerlength + window_size + '00 00' +
                  urgent_pointer).replace(' ', '')
    segment_cs = ' '.join(segment_cs[i:i + 2]
                          for i in range(0, len(segment_cs), 2))
    checksum_calculated = cs(segment_cs)
    return(source_port + destination_port + sequence_number +
           acknowledgement_number + TCP_headerlength + window_size +
           checksum_calculated + urgent_pointer).replace(' ', '')


def syn_sender(destination_MAC=dest_mac,
               source_MAC=src_mac,
               protocol3=proto3,
               version_headerlength=ver_ihl,
               TOS=tos,
               total_length=total_len,
               ID=id,
               flags_fragmentation_offset=flags,
               TTL=ttl,
               protocol4=proto4,
               source_IP=src_ip,
               destination_IP=dest_ip,
               source_port=src_port,
               destination_port=dest_port,
               sequence_number=seq_num,
               acknowledgement_number=ack,
               TCP_headerlength=tcp_hl,
               window_size=win_size,
               urgent_pointer=up):
    return sender(frame_calc(destination_MAC, source_MAC, protocol3) +
                  datagram_calc(version_headerlength, TOS, total_length,
                  ID, flags_fragmentation_offset, TTL, protocol4,
                  source_IP, destination_IP) +
                  segment_calc(source_IP, destination_IP, protocol4,
                  source_port, destination_port, sequence_number,
                               acknowledgement_number, TCP_headerlength,
                               window_size, urgent_pointer),
                  interface) == 54


if __name__ == '__main__':
    if syn_sender():
        print(f'Sent TCP SYN packet to {lines[0][:-1]} on {interface}')
