#!/bin/sh

pcap="$1"
trace=traces/$(readlink -f "$pcap" | grep -E -o '(/[^/]+){,3}$' | sed -E -e 's@^/@@' -e 's@/@_@g' -e 's@(pcap(ng)?)(\.gz)?$@@')txt

set -x
./generate-trace.sh "$pcap" > "$trace"
