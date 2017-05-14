#!/usr/bin/env python

from __future__ import print_function

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import json
import sys

matplotlib.rc('font', family='Open Sans', size=18)
matplotlib.rc('axes', labelweight='bold')
plt.figure(figsize=(11.69, 8.27), dpi=150)

data_file, graph_file = sys.argv[1:3]

data = json.loads(open(data_file).read())
histogram = dict((int(k), int(v)) for (k, v) in data.items())

# text
total_packets = sum(k * v for (k, v) in histogram.items())
for queries, count in histogram.items():
    packets = queries * count
    print("%d\t%d (%.03f %%)" % (queries, count, float(packets)/total_packets * 100))

# graph
plt.bar(histogram.keys(), histogram.values(), align='center', log=True)
plt.xlabel('Queries per packet')
plt.ylabel('Number of packets')

# more tight
plt.xlim(min(histogram.keys()) - 1, 51)
plt.tight_layout()

plt.savefig(graph_file, format="png")
