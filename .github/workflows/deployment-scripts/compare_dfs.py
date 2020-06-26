# Usage: python compare_dfs.py /path/to/df_new /path/to/df_old
#
# Returns non-zero exit value if the new df does not match the old one

import sys
import pandas as pd

# Get CSV paths
staged_csv_path = sys.argv[1]
master_csv_path = sys.argv[2]

print("[*] Reading staged CSV ({}), and master CSV ({})...".format(
    staged_csv_path, master_csv_path))

# Read CSVs into DFs and parse dates
df_staged = pd.read_csv(staged_csv_path, sep=',', parse_dates=["Day"])
df_staged.loc[:, "Day"] = pd.to_datetime(df_staged["Day"], 
                            format="y%m%d").dt.date

df_master = pd.read_csv(master_csv_path, sep=',', parse_dates=["Day"])
df_master.loc[:, "Day"] = pd.to_datetime(df_master["Day"], 
                            format="y%m%d").dt.date

# Do Checks 
print("[*] Checking columns...")
if set(df_staged.columns) != set(df_master.columns): 
    print("[E] Mismatching columns detected in {}: {} and {}".format(
        str(set(df_staged.columns).difference(set(df_master.columns))),
        str(set(df_master.columns).difference(set(df_staged.columns))),
        staged_csv_path))
    print("[E] Refusing to auto-merge...")
    sys.exit(-1)

# Success
print("[*] Success. Accepting changes!")

