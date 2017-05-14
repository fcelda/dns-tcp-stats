#!/bin/sh

pcap=$1
[ -z "$pcap" ] && exit 1

# -e _ws.col.Source
# -e _ws.col.Destination
# -e ip.src
# -e ip.dst

set -x
exec tshark -2 -r "$pcap" -T fields \
	-E header=y -E separator=/t -E quote=n -E occurrence=a -E aggregator=, \
	-e frame.time_relative -e tcp.stream -e ip.src -e ipv6.src -e tcp.srcport -e ip.dst -e ipv6.dst -e tcp.dstport -e dns.id -e dns.flags.response -e dns.qry.type \
	-Y tcp -R '!tcp.analysis.retransmission'
