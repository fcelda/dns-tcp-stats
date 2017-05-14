#!/usr/bin/env python

from __future__ import print_function
import collections
import json
import sys
import ipaddress

agg = dict()

def agg_ip(ip):
    mask = 48 if ":" in ip else 16
    addr = "%s/%d" % (ip, mask)
    net = ipaddress.ip_network(unicode(addr), strict=False)
    return str(net)

for arg in sys.argv[1:]:
    with open(arg) as f:
        data = json.loads(f.read())

        for ip, hist_mean in data.items():
            client = agg_ip(ip)

            c = agg.setdefault(client, dict())
            for k, values in hist_mean.items():
                c.setdefault(k, [])
                c[k].extend(values)

print(json.dumps(agg))
