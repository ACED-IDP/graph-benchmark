#!/usr/bin/env python

import yaml
import sys
import subprocess

if __name__ == "__main__":
    cfg = sys.argv[1]
    data = sys.argv[2]
    with open(cfg) as handle:
        config = yaml.safe_load(handle)

    for name, info in config["servers"].items():
        rpc = info["rpc"]
        graph = info["graph"]
        print(name, info["rpc"])

        subprocess.run( ["grip", "drop", "--host", rpc, graph] )
        subprocess.run( ["grip", "create", "--host", rpc, graph] )
        subprocess.run( ["grip", "load", "--host", rpc, graph, "--dir", data] )
    