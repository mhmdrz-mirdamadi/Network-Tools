#!/bin/bash

dest_ip=$1
dest_port=$2
interface=$3
src_port=$4
src_ip=`ip route show dev $interface | grep "kernel scope link src" | awk {'print $7'}`
src_ip="${src_ip//$'\n'/}"
src_mac=`ip link show $interface | grep "link/ether" | awk {'print $2'}`
src_mac="${src_mac//:/ }"
gateway_ip=`ip route list|grep "default"|awk {'print $3'}`
gateway_mac=`arp $gateway_ip | awk {'print $3'}`
gateway_mac="${gateway_mac: -17}"
gateway_mac="${gateway_mac//:/ }"

printf "$dest_ip\n$dest_port\n$src_ip\n$src_port\n$interface\n$src_mac\n$gateway_mac" > info.txt