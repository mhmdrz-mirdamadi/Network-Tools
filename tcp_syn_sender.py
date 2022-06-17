from socket import inet_aton
from checksum import cs
from pkt_sender import sender

lines: list
with open('info.txt', 'r') as fd:
    lines = fd.readlines()


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
cs3 = '00 00'  # IP header checksum
src_ip = inet_aton(lines[2]).hex()  # source IP address
dest_ip = inet_aton(lines[0]).hex()  # destination IP address

src_port = '%04x' % int(lines[3])  # source port
dest_port = '%04x' % int(lines[1])  # destination port
seq_num = '17 49 30 d1'  # sequence number
ack = '00 00 00 00'  # acknowledgement number
tcp_hl = '50 02'  # TCP header length and flags
win_size = '72 10'  # window size
cs4 = '00 00'  # TCP header checksum
up = '00 00'  # urgent pointer


def frame_calc():
    # Ethernet Frame
    return (dest_mac + src_mac + proto3).replace(' ', '')


def datagram_calc():
    # IP Datagram
    datagram_cs = (ver_ihl + tos + total_len + id +
                   flags + ttl + proto4 + cs3 + src_ip + dest_ip).replace(' ', '')
    datagram_cs = ' '.join(datagram_cs[i:i + 2]
                           for i in range(0, len(datagram_cs), 2))
    cs3_calculated = cs(datagram_cs)
    return(ver_ihl + tos + total_len + id +
           flags + ttl + proto4 + cs3_calculated + src_ip + dest_ip).replace(' ', '')


def segment_calc():
    # TCP Segment
    pseudo_header = src_ip + dest_ip + '00' + proto4 + '00 14'
    segment_cs = (pseudo_header + src_port + dest_port + seq_num + ack +
                  tcp_hl + win_size + cs4 + up).replace(' ', '')
    segment_cs = ' '.join(segment_cs[i:i + 2]
                          for i in range(0, len(segment_cs), 2))
    cs4_calculated = cs(segment_cs)
    return(src_port + dest_port + seq_num + ack +
           tcp_hl + win_size + cs4_calculated + up).replace(' ', '')


if __name__ == '__main__':
    print(sender(frame_calc() + datagram_calc() +
                 segment_calc(), lines[4][:-1]))
