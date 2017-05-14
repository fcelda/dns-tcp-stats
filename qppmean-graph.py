#!/usr/bin/env python

from __future__ import print_function

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import json
import sys
import random
import collections

matplotlib.rc('font', family='Open Sans', size=18)
matplotlib.rc('axes', labelweight='bold')
plt.figure(figsize=(11.69, 8.27), dpi=150)

data_file, graph_file = sys.argv[1:3]

data = json.loads(open(data_file).read())

for client, _histogram in data.items():
    if client != "74.125.0.0/16":
        continue

    histogram = dict((int(k), v) for k, v in _histogram.items())
    plt.boxplot(histogram.values(), labels=histogram.keys(), sym="")

plt.xlabel('Queries per connection')
plt.ylabel('Time between queries (seconds)')

plt.tight_layout()

plt.savefig(graph_file, format="png")
