#!/usr/bin/env python

from __future__ import print_function
import collections
import json
import sys

histogram = collections.Counter()

for arg in sys.argv[1:]:
    with open(arg) as f:
        data = json.loads(f.read())

        for _queries, _sessions in data["histogram"].items():
            queries, sessions = int(_queries), int(_sessions)
            histogram[queries] += sessions

print(json.dumps(dict(histogram)))
