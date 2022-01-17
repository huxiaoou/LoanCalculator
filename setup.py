import os
import sys
import datetime as dt
import numpy as np
import pandas as pd
import argparse

pd.set_option("display.width", 0)
# pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", "{:.2f}".format)

project_data_dir = os.path.join(".", "data")
