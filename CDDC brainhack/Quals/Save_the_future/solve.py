from scapy.all import rdpcap, TCP, Raw
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def dump_tcp_payloads(pcap_file):
    packets = rdpcap(pcap_file)        
    count = 0
    tcp_payloads = []
    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            tcp_payload = pkt[Raw].load
            tcp_payloads.append(tcp_payload)
    return tcp_payloads

tcp_payloads = dump_tcp_payloads("Alice_Bob_traffic.pcap")
leaked = "0XXXX000XX010XXXX0XX1011X11XX0110X1X1XXXXXX111011XX11XX1X1X1X0010X1111X0X110XXX1X11001001X10X1001XXXXXX0XXXXXXX01X1X110000X10X11XX0101XX010XXX1XXXX0XXX0X01XX1X10XX110XX111XXXX0X1XX0X0X010X01XXX1X1X0X0XXXXX00X1XXX10X111XX110X01XXXXX00X011100X0101XX1XXXX0001"
known = ''.join([i for i in leaked if i in '01'])
encrypted_key = b'j\xde\xc6\xee\xae\x8b\xcfi\xbd\xba\x1b\x05\x82}c\xf3\xc6\xd0b\xa1\x8c\xb1h\xc2\xe2\xbe!Z\x81N7]\xf2\x8a\xb1-\xa0\xba\xc4\x8f\x95\x8b\x9f6\x1e\x01K\xb9\x93\xaf<\xe3GF\xe1\xc2\xff\xc5\xec\x9cL\x14\x0c\x99'
key = int(known[8:], 2).to_bytes(16, 'big')
iv = b'\x00' * 16
cipher = AES.new(key, AES.MODE_CBC, iv)

unpadded = unpad(cipher.decrypt(tcp_payloads[35]), 16)
# print(aes_key[])
aes_key = unpadded[16:] 
iv = unpadded[:16]

tmp = AES.new(aes_key, AES.MODE_CBC, iv).decrypt(tcp_payloads[37])
print(tmp)
# cipher = AES.new(aes_key, AES.MODE_CBC, iv)
# print(cipher.decrypt(enc))