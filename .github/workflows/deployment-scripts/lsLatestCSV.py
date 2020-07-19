# Usage: lsLatestCSV prefix dir
#   Finds the latest CSV in current directory with prefix prefix using 
#   DELPHI team's dating convention

import os
import sys
import datetime
from datetime import timedelta

prefix = sys.argv[1]
new_dir = sys.argv[2]

os.chdir(new_dir)

print("[*] Looking for latest CSV with prefix: " + prefix)

targets = []
for fname in os.listdir():
    if fname.startswith(prefix):
        targets.append(fname)

print("[*] Candidates: " + str(targets))
date = datetime.datetime.now()
delta = timedelta(days=1) 

target = None
while target is None and date.year >= 2020: 
    date = date - delta
    match = date.strftime("%Y%m%d")
    candidate = prefix + match + ".csv" 
    if candidate in targets: 
        target = prefix + match + ".csv"

if target is None: 
    print("[*] Could not find latest CSV with prefix " + prefix)
    sys.exit(1)

print("[*] Found latest CSV: " + target + "...")

# This last print statement can get fed into bash through tail pipe
print(target)

