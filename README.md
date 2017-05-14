# tcp-dns-stats

No state-of-the-art Python. Just bunch of scripts to get elementary information about DNS over TCP queries from _pcap_ packet captures.

## Dependencies

- tshark
- Python 2 (see _requirements.txt_)

## Scripts

Convert pcap to a trace (CSV list) that can be later read by the other scripts in this repository:

```sh
$ generate-trace.sh ./capture.pcapng > trace.txt
$ cat trace.txt
frame.time_relative	tcp.stream	ip.src	ipv6.src	tcp.srcport	ip.dst	ipv6.dst	tcp.dstport	dns.id	dns.flags.response	dns.qry.type
0.000000000	0	203.0.113.123		51346	198.51.100.2		53
0.000040000	0	198.51.100.2		53	203.0.113.123		51346
0.001024000	0	203.0.113.123		51346	198.51.100.2		53
0.001113000	0	203.0.113.123		51346	198.51.100.2		53	0x0000e3b1	0	1
0.001135000	0	198.51.100.2		53	203.0.113.123		51346
0.002402000	0	198.51.100.2		53	203.0.113.123		51346	0x0000e3b1	1	1
0.003386000	0	203.0.113.123		51346	198.51.100.2		53
0.003432000	0	203.0.113.123		51346	198.51.100.2		53
0.003601000	0	198.51.100.2		53	203.0.113.123		51346
0.004587000	0	203.0.113.123		51346	198.51.100.2		53
...
```

Queries per session (connection) stats:

```sh
$ ./qps-analyse.py trace_1.txt > trace_1.json
$ ./qps-analyse.py trace_2.txt > trace_2.json
$ ./qps-sum-clients.py trace_*.json > sum_clients.json
$ ./qps-sum-histogram.py trace_*.json > sum_histogram.json
$ ./qps-graph-histogram.py sum_histogram.{json,png,txt}
$ cat sum_histogram.txt
# q/session	count (relative)	queries (relative)
0	24314732 (37.3044 %)	0 (0.0000 %)
1	37740432 (57.9024 %)	37740432 (80.6956 %)
2	1668266 (2.5595 %)	3336532 (7.1341 %)
...
$ ./qps-txt-clients.py sum_clients.json > info_clients.txt
$ cat info_clients.txt
# asn	queries_info	sessions_info	avg_qpsession	queries	sessions
AS 1111 (Corp A)	2 (0.000 %)	1 (0.000 %)	2.00	2	1
AS 2222 (Corp B)	8 (0.000 %)	4 (0.000 %)	2.00	8	4
AS 3333 (Corp C)	2 (0.000 %)	1 (0.000 %)	2.00	2	1
...
```

Queries per packet (not connection) stats:

```sh
$ qpp-analyse.py trace_1.txt > qpp_1.json
$ qpp-analyse.py trace_2.txt > qpp_2.json
$ qps-sum-clients qpp_*.json > sum_clients_qpp.json
$ qpp-sum-histogram qpp_*.json > sum_histogram_qpp.json
$ qpp-graph-histogram.py sum_histogarm_qpp.json qpp.png
```

Mean time between queries:

```sh
$ qppmean-analyse.py trace_1.txt > mean_1.json
$ qppmean-analyse.py trace_2.txt > mean_2.json
$ qppmean-sum.py mean_1.json mean_2.json > sum_mean.json
$ qppmean-graph.py sum_mean.json mean.png
```

Parallelize analysing traces:

```sh
$ command ls -1 ditl2016/org/server/*.pcap | parallel -j16 -n1 par-pcap2trace.sh ./traces
```

```sh
$ command ls -1 traces/*.txt | parallel -j16 -n par-analyse-trace.sh ./qps-analyse.py ./qps.results
```

## License

The content of this repository is licensed under Apache License 2.0
