# Usage: python check_global.py /path/to/df_new /path/to/df_old date_col NAN_tolerance skip_check 
#
# Returns non-zero exit value if the new Global.csv dataframe fails a check

import sys
import pandas as pd
import datetime
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Checks DELPHI CSV files')
parser.add_argument("staged_csv", type=str, 
                    help="The CSV that is staged and will replace master")
parser.add_argument("master_csv", type=str, 
                    help="The CSV master CSV that is currently deployed")
parser.add_argument('--mape-tolerance', dest="mape_tolerance", type=float, default=0.1,
                    help='The tolerence of NANs in the mape column in decimanl percent')
parser.add_argument('--date-col', dest='date_col', default="Day",
                    help='The datetime column of the CSV. For Global.csv should be "Day"' + 
                        ' for Parameters_Global.csv should be "Data Start Date"')
parser.add_argument('--skip-checks', dest='skipping', nargs="+", type=int, default=[],
                    help='A list of checks to skip for this run')
parser.add_argument('--allow-neg', dest='allow_neg', nargs="+", type=str, default=[],
                    help='A list of column names which are allowed to have negative numbers.')

args = parser.parse_args()

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
    info_check("Reading staged CSV ({}), and master CSV ({})".format(
          args.staged_csv, args.master_csv))

    df_staged = pd.read_csv(args.staged_csv, sep=',', parse_dates=[args.date_col])
    df_master = pd.read_csv(args.master_csv, sep=',', parse_dates=[args.date_col])
except: 
    fail_check("Failed to read CSVs or input arguments")

# Parse Dates 
try:
    df_staged.loc[:, args.date_col] = pd.to_datetime(df_staged[args.date_col], 
                                format="y%m%d").dt.date
    df_master.loc[:, args.date_col] = pd.to_datetime(df_master[args.date_col], 
                                format="y%m%d").dt.date
except: 
    fail_check("Failed to parse dates")

#
# Check #1: "Check the number of columns and column 
#            names in each dataset pushed"
#
if 1 in args.skipping: 
    info_check("Skipping Matching Columns Check")
else: 
    info_check("Checking matching columns")
    if set(df_staged.columns) != set(df_master.columns): 
        fail_check("Mismatching columns detected in {}: {} and {}".format(
            args.staged_csv,
            str(set(df_staged.columns).difference(set(df_master.columns))),
            str(set(df_master.columns).difference(set(df_staged.columns)))))

#
# Check #2: "Check if in each column there are no NA values"
#
if 2 in args.skipping: 
    info_check("Skipping NaNs check")
else: 
    info_check("Checking for NaNs")
    for c in df_master.columns: 
        num_na = df_staged[c].isnull().sum()
        total = df_staged[c].count() 
        if c == "MAPE" and num_na > 0 and num_na / total < args.mape_tolerance:
            info_check("Found MAPE NANs: " + str(num_na / total * 100) + "%")
            continue
        if c == "Total Detected True" or c == "Total Detected Deaths True": 
            continue
        if num_na > 0:
            rows = list(df_staged[df_staged.isnull().any(axis=1)].index.to_numpy())
            fail_check("Found NaN entries in {}, at rows {}".format(
                args.staged_csv, rows))
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
if 3 in args.skipping: 
    info_check("Skipping numbers of areas check")
else: 
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
if 4 in args.skipping:
    info_check("Skipping date threshold check")
else: 
    date_thresh = datetime.date(2020, 10, 15)
    info_check("Checking that all latest predictions are >= {}".format(\
                str(date_thresh)))

    # Get the last dates from each area
    latest_dates = df_staged.groupby(["Continent", "Country", "Province"])[args.date_col].tail(1)
    if not (latest_dates >= date_thresh).all(): 
        fail_check("The staged df contains outdated data, " + 
                   "with latest date {}".format(latest_dates.min()))

#
# Check #5: "Check for any negative numerical values"
#
if 5 in args.skipping: 
    info_check("Skipping negative numbers check")
else:
    info_check("Looking for negative numbers")
    def func(s): 
        to_num = pd.to_numeric(s, errors='coerce')
        if not to_num.isnull().any() and (to_num >= 0).all():
            return True
        if to_num.isnull().any():
            return True
        if s.name in args.allow_neg: 
            info_check("Found negatives but making an exception for " + s.name)
            return True
        info_check("Found negative values on these rows")
        info_check("\n" + str(s[s < 0]))
        return False
    if (df_staged.apply(func) == False).any():
        fail_check("Negative values were found")

# Success
info_check("Success! Staged CSV passed Checks 1-5")

