#!/usr/bin/env python

import yaml
import time
import sys
import subprocess

if __name__ == "__main__":
    cfg = sys.argv[1]
    with open(cfg) as handle:
        config = yaml.safe_load(handle)

    procs = []
    for name, info in config["servers"].items():
        print(name, info["config"])
        p = subprocess.Popen( ["grip", "server", "--config", info["config"]] )
        procs.append(p)
    
    done = False
    while not done:
        try:
            time.sleep(.3)
        except KeyboardInterrupt:
            done = True