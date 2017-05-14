#!/usr/bin/env python

from __future__ import print_function
import collections
import json
import sys
import ipaddress

clients = dict()

def agg_ip(ip):
    mask = 48 if ":" in ip else 16
    addr = "%s/%d" % (ip, mask)
    net = ipaddress.ip_network(unicode(addr), strict=False)
    return str(net)

for arg in sys.argv[1:]:
    with open(arg) as f:
        data = json.loads(f.read())

        for ip, _histogram in data["clients"].items():
            client = agg_ip(ip)
            __histogram = dict((int(k), int(v)) for (k, v) in  _histogram.items())
            histogram = collections.Counter(__histogram)

            clients.setdefault(client, collections.Counter())
            clients[client] += histogram

print(json.dumps(clients))
