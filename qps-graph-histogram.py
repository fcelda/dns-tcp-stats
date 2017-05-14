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

data_file, graph_file, num_file = sys.argv[1:4]

data = json.loads(open(data_file).read())
histogram = dict((int(k), int(v)) for (k, v) in data.items() if int(k) < 80)

# text info
total_sessions = sum(v for v in histogram.values())
total_queries = sum((k * v) for (k, v) in histogram.items())

with open(num_file, "w") as txt:
    print("# q/session\tcount (relative)\tqueries (relative)", file=txt)
    for k, v in histogram.items():
        print("%d\t%d (%.04f %%)\t%d (%.04f %%)" % (k, v, float(v)/total_sessions*100, k * v, float(k * v)/total_queries*100), file=txt)

# graph
plt.bar(histogram.keys(), histogram.values(), align='center', log=True)
plt.xlabel('Queries per connection')
plt.ylabel('Number of connections')

#plt.xticks(range(0,51,5))
plt.ylim(0, 1e7)
plt.xlim(min(histogram.keys()) - 1, max(histogram.keys()) + 1)

plt.tight_layout()

plt.savefig(graph_file, format="png")
