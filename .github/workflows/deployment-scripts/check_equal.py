# Usage: python check_equal.py /path/to/df_one /path/to/df_two
#
# Returns non-zero exit value if the dataframes are not equal

# Handles Check #5: "Check that Global.csv file corresponds 
#                    exactly to the latest Global_<date>.csv 
#                    file in the repo"

import sys
import pandas as pd

# Fail function
def fail_check(reason):
    print("[E] {}".format(reason))
    print("[E] Refusing to auto-merge!")
    sys.exit(1)


# Info function
def info_check(info):
    print("[*] {}...".format(info))


# Read CSVs into DFs
try: 
    # Get CSV paths
    df_one_path = sys.argv[1]
    df_two_path = sys.argv[2]

    info_check("Reading staged CSV ({}), and master CSV ({})".format(
                df_one_path, df_two_path))

    df_one = pd.read_csv(df_one_path, sep=',', parse_dates=["Day"])
    df_two = pd.read_csv(df_two_path, sep=',', parse_dates=["Day"])
except: 
    fail_check("Failed to read CSVs")

info_check("Checking for equality")
if not df_one.equals(df_two): 
    fail_check("Dataframes {} and {} are not equal".format(
                df_one_path, df_two_path))

# Success
info_check("Success! The dataframes are equal")

