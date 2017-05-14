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

    flows.setdefault(packet["flow"], {
        "client": packet["client"],
        "qtypes": set(),
        "packets": 0,
        "queries": 0,
        "time_start": packet["time"],
        "time_query": [],
        "time_end": None,
    })

    flow = flows[packet["flow"]]
    flow["qtypes"] |= set(packet["dns_qtype"])
    flow["packets"] += 1
    flow["time_end"] = packet["time"]

    if True in packet["dns_query"]:
        flow["queries"] += len(packet["dns_query"])
        flow["time_query"].append(packet["time"])

# delete flows with unassigned types, AXFR/IXFR, or ANY
def standard_type(type):
    return 1 <= type and type <= 258 and type not in [251, 252, 255]

flows = dict((k, v) for (k, v) in flows.items() if all(standard_type(t) for t in v["qtypes"]))

# histogram for each client
result = {}
for flow, data in flows.items():
    if data["queries"] > 1:
        # time between queries
        means = [round(b - a, 5) for a, b in zip(data["time_query"], data["time_query"][1:])]

        r = result.setdefault(data["client"][0], dict())
        t = r.setdefault(data["queries"], [])
        t.extend(means)

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, collections.Counter):
            return dict(obj)
        else:
            return json.JSONEncoder.default(self, obj)

print(json.dumps(result, cls=Encoder))
