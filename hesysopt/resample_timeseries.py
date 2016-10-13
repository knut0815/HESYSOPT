# -*- coding: utf-8 -*-
"""
This module is for resampling the sequence csv-data file. The file is read
from the specified directory, resampled and, written back to the directory
as XH_sample.csv, where X are the sampled hours.

"""
import pandas as pd
import os

path = 'examples/simple_example/'
files = os.listdir(path)
seq_file = [i for i in files if 'seq' in i][0]

seq = pd.read_csv(os.path.join(path, seq_file), header=[0, 1, 2, 3, 4])

# set timeindex
seq.index = pd.date_range(start='2011', freq='H', periods=len(seq.index))
# concert columns to numeric values
for col in seq:
    seq[col] = seq[col].astype(float)

for i in ['2H', '3H', '4H', '5H', '6H']:
# resample dataframes
    seq_sampled = seq.resample(i, how='mean')
    seq_sampled.to_csv(os.path.join(path, i+'_sample.csv'), index=False)
#seq = pd.read_csv(os.path.join(path, '4h_sample.csv'))

# gemerate with original timeseries for plotting purposes
#h2 = seq2h[col].repeat(2)
h4 = seq_sampled[col].repeat(6)
#h2.index = seq.index
h4.index = seq.index

plot_data = pd.concat([h4, seq[col]], axis=1)
plot_data.iloc[1:268].plot(drawstyle='steps')
