from scapy.all import *

def pkt_display(packet):
	if "ip" in packet[0][1].summary().lower():
		print "...........IP Packet", packet
		#validateAndSendIpBackRequest(packet)
		
	else
		print "Not a IP packet..."
		

sniff(iface = eth0, prn=pkt_display, filter='host 172.31.129.22',store=0, count=0)
