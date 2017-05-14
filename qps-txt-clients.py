#!/usr/bin/env python

from __future__ import print_function
import collections
import json
import maxminddb
import operator
import sys
import locale

locale.setlocale(locale.LC_NUMERIC, 'en_US')

geo = maxminddb.open_database("./GeoLite2-ASN.mmdb")

raw = open(sys.argv[1]).read()
data = json.loads(raw)

summary = dict()

def net_to_asn(net):
    addr = net.split("/")[0]
    info = geo.get(addr)
    if info:
        asn = info.get("autonomous_system_number", None)
        org = info.get("autonomous_system_organization", None)
    else:
        print("unknown as for %s" % net, file=sys.stderr)
        asn = None
        org = None
    return (asn, org)

for net, hist in data.items():
    asn, as_name = net_to_asn(net)

    rec = summary.setdefault(asn, dict(name=as_name, queries=0, sessions=0))
    rec["queries"] += sum(int(k) * int(v) for k, v in hist.items())
    rec["sessions"] += sum(int(v) for v in hist.values())

sum_queries = sum(data["queries"] for data in summary.values())
sum_sessions = sum(data["sessions"] for data in summary.values())

print("#asn\tqueries_info\tsessions_info\tavg_qpsession\tqueries\tsessions")
for asn, data in summary.items():
    as_info = "AS %d (%s)" % (asn, data["name"]) if asn else "-"
    q_info = "%s (%.03f %%)" % (locale.format("%d", data["queries"], grouping=True), float(data["queries"])/sum_queries * 100)
    s_info = "%s (%.03f %%)" % (locale.format("%d", data["sessions"], grouping=True), float(data["sessions"])/sum_sessions * 100)

    print("%s\t%s\t%s\t%.02f\t%d\t%d" % (as_info, q_info, s_info, float(data["queries"]) / data["sessions"], data["queries"], data["sessions"]))
