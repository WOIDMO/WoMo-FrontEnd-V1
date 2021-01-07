# MIT-License
#
# Copyright 2020 World Infectious Disease Monitoring Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy
# Source https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/muzy-jte6
# JS sample https://episphere.github.io/mortalitytracker/#cause=allcause&state=All%20States

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.cdc.gov", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata("data.cdc.gov",
                  "hBx6CTw35fMrJCELWjjpqBDgn",
                  "it@woidmo.org",
                  "L33L8QGMGGDh8nb")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#First:  fetch('https://data.cdc.gov/resource/3yf8-kanr.json?$limit=10000')
#Second: fetch('https://data.cdc.gov/resource/3yf8-kanr.json?$limit=10000&$offset=10000')
results = client.get("3yf8-kanr", limit=10000, offset=10000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
print (results_df)

results_df.to_csv("../data/2014w1-2018w52-2.csv", index=False)
