#!/usr/bin/env python

from __future__ import print_function
import collections
import json
import sys

histogram = collections.Counter()

for arg in sys.argv[1:]:
    with open(arg) as f:
        data = json.loads(f.read())

        for _client, _histogram in data.items():
            h = dict((int(k), int(v)) for (k, v) in _histogram.items())
            histogram += collections.Counter(h)


print(json.dumps(dict(histogram)))
