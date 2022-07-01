# Network Tools

## 0. Introduction

In this project, we want to bypass the entire TCP/IP protocol stack within the operating system and send anything directly (any sequence of zeros and ones) through one of our host machine interfaces or show anything received by it. Finally, using these, we try to make a **_mini-wireshark_** and a **_mini-nmap_**.

## 1. Send any packet

Using the `pkt_sender.py`, any packet can be sent through one of the interfaces of your host system. This packet is at the link-layer level and must be in the following format to be valid:
| # | Destination MAC Address | Source MAC Address | EtherType | Payload
| :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| **Size** | 6 bytes | 6 bytes | 2 bytes | Up to 1500 bytes
| **Sample Format** | _F3054290A2C6_ | _5E0781A2BB0D_ | _0080_ |

You can also use the command below to view a list of your system interfaces:

```
$ ip link

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether ff:aa:22:88:77:dd brd ff:ff:ff:ff:ff:ff
```

### Example

Sending an empty packet through the _eth0_ interface:

```
$ sudo python3 pkt_sender.py

What is your packet content? F3054290A2C65E0781A2BB0D0080
Which interface do you want to use? eth0
Sent 14-byte packet on eth0
```

## 2. Send TCP SYN packet

In this part, `tcp_syn_sender.py` uses `checksum.py` that is used to calculate the checksum, and also `pkt_sender.py` described in the previous section, to create TCP SYN packets and send them to a specific destination.  
`tcp_syn_sender.py` receives its packet sending information from `info.txt` located in the same path. The format of this file is specified in `info.txt.sample`. Here are some commands to get this information:

1. Use _dig_ to get IP address of a server
   > _example.com_ IP address: 93.184.216.34

```
$ dig example.com

; <<>> DiG 9.18.1-1ubuntu1.1-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46585
;; flags: qr rd ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            0       IN      A       93.184.216.34

;; Query time: 30 msec
;; SERVER: 20.20.20.20#53(20.20.20.20) (UDP)
;; WHEN: Fri Jul 01 13:08:43 +0430 2022
;; MSG SIZE  rcvd: 56
```

2. Use _ifconfig_ to get the IP & MAC address of an interface
   > _eth0_ IP address: 20.20.20.20  
   > _eth0_ MAC address: ff:aa:22:88:77:dd

```
$ ifconfig

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 20.20.20.20  netmask 255.255.240.0  broadcast 20.20.20.255
        inet6 aaaa::333:bbbb:cccc:4444  prefixlen 64  scopeid 0x20<link>
        ether ff:aa:22:88:77:dd  txqueuelen 1000  (Ethernet)
        RX packets 85620  bytes 369221890 (369.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 70860  bytes 5062108 (5.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

3. Use _arp_ to get the gateway router MAC address
   > _eth0_ gateway MAC address: bb:66:44:33:00:cc

```
$ arp `ip route list|grep "default"|awk {'print $3'}` | awk {'print $3'}

HWaddress
bb:66:44:33:00:cc
```

It is also possible to generate `info.txt` automatically by calling `ifinfo.sh` shell script and passing _destination IP address, destination port number, interface, and source port number_ respectively as shown below:

```
$ bash ifinfo.sh 93.184.216.34 80 eth0 3000
```

### Example

```
$ sudo python3 tcp_syn_sender.py

Sent TCP SYN packet to 93.184.216.34 on eth0
```

## 3. mini-Wireshark

Wireshark is a packet sniffer and analysis tool. It captures network traffic on the local network and stores that data for offline analysis.  
In this part, `miniwireshark.py`, which is a special-purpose Wireshark, receives all TCP SYN ACK packets that are sent to the host device and shows the sender's IP address and port number.

### Example

Run `miniwireshark.py` at the same time as `tcp_syn_sender.py` to demonstrate its functionality.

```
$ sudo python3 miniwireshark.py

Port 80 is open on 93.184.216.34
```

## 4. mini-Nmap

Nmap is a network scanner to discover hosts and services on a computer network by sending packets and analyzing the responses.  
In this section, `mininmap_sender.py` and `mininmap_sender_tcpsocket.py` are written with the aim of scanning a range of ports of a server with a specific IP by sending TCP SYN packets. By running `miniwireshark.py` simultaneously, it could be shown which services the destination server provides.

`mininmap_sender.py` uses `tcp_syn_sender.py` to send TCP SYN packets.

`mininmap_sender_tcpsocket.py` does the same thing by creating TCP sockets as quickly as possible. The noteworthy point in this program is to use the timeout as manual so that by default this time is equal to 5 milliseconds, but when running the program with the argument t, this value can be set as desired. (It is recommended not to use values less than 5 milliseconds)

### Example

```
$ sudo python3 mininmap_sender.py

What is the target IP address? 8.8.8.8
Which ports do you want to scan? 50-55
Sent TCP SYN packet to port 50
Sent TCP SYN packet to port 51
Sent TCP SYN packet to port 52
Sent TCP SYN packet to port 53
Sent TCP SYN packet to port 54
```

Running `mininmap_sender_tcpsocket.py` with a timeout of 8 milliseconds:

```
$ sudo python3 mininmap_sender_tcpsocket.py -t 8

What is the target IP address? 8.8.8.8
Which ports do you want to scan? 50-55
Sent TCP SYN packet to port 50
Sent TCP SYN packet to port 51
Sent TCP SYN packet to port 52
Sent TCP SYN packet to port 53
Sent TCP SYN packet to port 54
```
