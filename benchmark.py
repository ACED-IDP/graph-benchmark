#!/usr/bin/env python

import sys
import time
import yaml
import gripql
import pandas as pd
import numpy as np
test_count = 10

if __name__ == "__main__":
    cfg = sys.argv[1]
    with open(cfg) as handle:
        config = yaml.safe_load(handle)

    servers = {}
    queries = {}
    results = {}
    for name, info in config["servers"].items():
        print(name, info["host"])
        conn = gripql.Connection(info["host"])
        G = conn.graph(info["graph"])

        results[name] = {}
        host_queries = {}
        for qname, code in config["queries"].items():
            code = code.replace("\n", "")
            #print(code)
            q = eval(code, {"G":G, "gripql":gripql})
            #print(q)
            host_queries[qname] = q
            results[name][qname] = []
        queries[name] = host_queries


    for server, squeries in queries.items():
        for name, query in squeries.items():
            for i in range(test_count):
                start = time.perf_counter()
                z = query.execute()
                stop = time.perf_counter()
                results[server][name].append(stop-start)

    out = {}
    for x, l in results.items():
        o = {}
        for y, v in l.items():
            o[y] = np.mean(v)
        out[x] = o
    df = pd.DataFrame(out)
    #df.to_csv(sys.stdout, sep="\t")
    print(df * 1000)
    print("----")
    print( (df.transpose() / df.max(axis=1)).transpose() )