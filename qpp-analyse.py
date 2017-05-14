#!/usr/bin/env python

from __future__ import print_function
import sys
import csv
import json
import collections
import ipaddress

def split_value(row, name, map_cb=None):
    value = row.get(name, "")
    values = value.split(",") if value != "" else []
    if map_cb is None:
        return values
    else:
        return [map_cb(v) for v in values]

def decode_row(row):
    if row["tcp.stream"] == "":
        return

    client = (row["ip.src"] or row["ipv6.src"], int(row["tcp.srcport"]))
    server = (row["ip.dst"] or row["ipv6.dst"], int(row["tcp.dstport"]))
    if client[1] == 53:
        client, server = server, client

    return {
        "flow": int(row["tcp.stream"]),
        "time": float(row["frame.time_relative"]),
        "client": client,
        "server": server,
        "dns_id": split_value(row, "dns.id"),
        "dns_query": split_value(row, "dns.flags.response", lambda flag: flag == "0"),
        "dns_response": split_value(row, "dns.flags.response", lambda flag: flag == "1"),
        "dns_qtype": split_value(row, "dns.qry.type", lambda type: int(type)),
    }

def private_ip(ip):
    return ipaddress.ip_address(unicode(ip)).is_private

packets = []
servers = set()
with open(sys.argv[1]) as cvsfile:
    reader = csv.DictReader(cvsfile, delimiter="\t", strict=True)
    for row in reader:
        packet = decode_row(row)
        if not packet:
            continue

        if private_ip(packet["client"][0]) or private_ip(packet["server"][0]):
            continue

        packets.append(packet)
        servers.add(packet["server"][0])

# count flows
flows = {}
for packet in packets:
    # skip server initiated connections
    if packet["client"][0] in servers:
        continue

    flows.setdefault(packet["flow"], {"qpp": collections.Counter(), "packets": 0, "client": packet["client"], "qtypes": set()})
    flow = flows[packet["flow"]]

    flow["packets"] += 1
    flow["qtypes"] |= set(packet["dns_qtype"])

    qcount = len([q for q in packet["dns_query"] if q])
    if qcount > 0:
        flow["qpp"][qcount] += 1

# delete flows with unassigned types, AXFR/IXFR, or ANY
def standard_type(type):
    return 1 <= type and type <= 258 and type not in [251, 252, 255]

flows = dict((k, v) for (k, v) in flows.items() if all(standard_type(t) for t in v["qtypes"]))

# histogram for each client
result = {}
for flow, data in flows.items():
    total_queries = sum(k * v for k, v in data["qpp"].items())
    if total_queries > 1:
        r = result.setdefault(data["client"][0], dict(packets=0, qpp=collections.Counter()))
        r["packets"] += data["packets"]
        r["qpp"] += data["qpp"]

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, collections.Counter):
            return dict(obj)
        else:
            return json.JSONEncoder.default(self, obj)

print(json.dumps(result, cls=Encoder))
