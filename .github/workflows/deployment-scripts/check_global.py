# Usage: python check_global.py /path/to/df_new /path/to/df_old
#
# Returns non-zero exit value if the new Global.csv dataframe fails a check

import sys
import pandas as pd
import datetime
import numpy as np


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
    staged_csv_path = sys.argv[1]
    master_csv_path = sys.argv[2]

    info_check("Reading staged CSV ({}), and master CSV ({})".format(
          staged_csv_path, master_csv_path))

    df_staged = pd.read_csv(staged_csv_path, sep=',', parse_dates=["Day"])
    df_master = pd.read_csv(master_csv_path, sep=',', parse_dates=["Day"])
except: 
    fail_check("Failed to read CSVs")

# Parse Dates 
try:
    df_staged.loc[:, "Day"] = pd.to_datetime(df_staged["Day"], 
                                format="y%m%d").dt.date
    df_master.loc[:, "Day"] = pd.to_datetime(df_master["Day"], 
                                format="y%m%d").dt.date
except: 
    fail_check("Failed to parse dates")

#
# Check #1: "Check the number of columns and column 
#            names in each dataset pushed"
#
info_check("Checking matching columns")
if set(df_staged.columns) != set(df_master.columns): 
    fail_check("Mismatching columns detected in {}: {} and {}".format(
        staged_csv_path,
        str(set(df_staged.columns).difference(set(df_master.columns))),
        str(set(df_master.columns).difference(set(df_staged.columns)))))

#
# Check #2: "Check if in each column there are no NA values"
#
info_check("Checking for NaNs")
if df_staged.isnull().values.any(): 
    rows = list(df_staged[df_staged.isnull().any(axis=1)].index.to_numpy())
    fail_check("Found NaN entries in {}, at rows {}".format(
                staged_csv_path, rows))

#
# Check #2.5: "as well as the type of the entries"
#
# This does not catch errors like putting an integer into a column of strings
# because the integer would be interpreted as a string. However, I think 
# that's okay because that would be a really unlikely error. It does catch 
# putting strings or other types in columns of numbers. 
info_check("Checking for matching datatypes")
for c in df_master.columns: 

    # Compute sets of unique types in this column
    unique_staged_types = set(df_staged[c].apply(lambda x: type(x)).unique())
    unique_master_types = set(df_master[c].apply(lambda x: type(x)).unique())

    # Check if the sets are equal
    if set(unique_staged_types) != set(unique_master_types): 
        fail_check("Mismatching datatypes detected")

#
# Check #3: "Check the number of areas we have (>= than certain number)"
#
info_check("Checking for correct number of areas")
areas = ["Continent", "Country", "Province"]
staged_unique = df_staged.apply(pd.Series.nunique)
master_unique = df_master.apply(pd.Series.nunique)
for area in areas: 
    info_check("Found {}/{} unique {}".format(staged_unique[area],
        master_unique[area], area))
    if staged_unique[area] < master_unique[area]:
        fail_check("The staged df has less unique areas " +
                   "({}) than master".format(area))

#
# Check #4: "Latest date predicted for each country should be >= 2020-10-15"
# 
date_thresh = datetime.date(2020, 10, 15)
info_check("Checking that all latest predictions are >= {}".format(\
            str(date_thresh)))

# Get the last dates from each area
latest_dates = df_staged.groupby(["Continent", "Country", "Province"]).Day.tail(1)
if not (latest_dates >= date_thresh).all(): 
    fail_check("The staged df contains outdated data, " + 
               "with latest date {}".format(latest_dates.min()))

# Success
info_check("Success! Staged CSV passed Checks 1-4")

