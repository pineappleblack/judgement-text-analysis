from tqdm import tqdm

import match_counter
import os
import pandas as pd
import sys
import traceback

if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode = 'fab'

ignore_courts = False
if len(sys.argv) > 2:
    if sys.argv[2] == 'ignore_courts':
        ignore_courts = True

directory = "output_files"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = "output_files/pairs_and_contents"
if not os.path.exists(directory):
    os.makedirs(directory)

with open('output_files/pairs_and_contents/!contents.html', 'w') as f:
    f.write('')

if not ignore_courts:
    try:
        df = pd.read_csv('input_files/annotation.csv')
        courts = df['court'].unique()
        for court in tqdm(courts):
            if isinstance(court, str):
                try:
                    match_counter.match_files([str(el)+'.txt' for el in list(df[df['court']==court]['Unnamed: 0'])], court, mode=mode)
                except:
                    traceback.print_exc()
                    exit()

    except:
        traceback.print_exc()
        print('Annotation was not found')
        match_counter.match_files(mode=mode)
else:
    match_counter.match_files(mode=mode)