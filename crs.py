import numpy as np
import pandas as pd
from dashboard import Crypto
#crypto recommendation system test (will be moved to website later on)
#Goal: find similarity from summarized features in list of cryptos

ticks = pd.read_csv("all_ticks.csv").drop("Unnamed: 0", axis = 1)


