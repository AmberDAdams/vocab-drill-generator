import config
import ctypes
import random
import argparse as ap
import pandas as pd
from datetime import datetime as dt
from shutil import copyfile

options = list(config.vocab_lists.keys())

parser = ap.ArgumentParser(description=f'Select a language file to use (options: {", ".join(options)}).')
parser.add_argument('lang', metavar='Language', type=str, nargs=1, choices=options,
                    help='The language to generate a word for.')
parser.add_argument('--numwords', '-n', type=int, help='The number of vocabulary words to generate.', default=5)

args = parser.parse_args()
chosen_language = args.lang[0].capitalize()
num_words_to_return = args.numwords

vocab_file_path = config.vocab_list_path + config.vocab_lists[chosen_language]
vocab_df = pd.read_csv(vocab_file_path)

#save a backup of the vocab file (written over each time)
copyfile(vocab_file_path, vocab_file_path.replace('.csv', ' BACKUP.csv'))

# if nextdate and/or NumPractices column does not exist, add it
if 'NextDate' not in vocab_df.columns:
    vocab_df['NextDate'] = dt.today()
if 'NumPractices' not in vocab_df.columns:
    vocab_df['NumPractices'] = 0

# if any words have been added since the last run
# fill NextDate with today's date and NumPractices with 0
vocab_df['NextDate'] = vocab_df['NextDate'].replace(r'^\s*$', dt.today(), regex=True)
vocab_df['NextDate'] = vocab_df['NextDate'].fillna(dt.today())
vocab_df['NumPractices'] = vocab_df['NumPractices'].replace(r'^\s*$', 0, regex=True)
vocab_df['NumPractices'] = vocab_df['NumPractices'].fillna(0)

# ensure NextDate and NumPractices are the proper datatypes
vocab_df['NextDate'] = vocab_df['NextDate'].apply(lambda x: dt.strptime(x, '%d/%m/%Y') if isinstance(x, str) else x)
vocab_df['NumPractices'] = vocab_df['NumPractices'].apply(lambda x: x if isinstance(x, int) else x)

# randomly select using date logic instead of just taking top
rows_available_to_practice = list(vocab_df.loc[vocab_df.NextDate.apply(lambda x: x<=dt.today())].index.copy())
rows_to_practice = random.choices(rows_available_to_practice, k=num_words_to_return)
vocab_to_practice = list(vocab_df.iloc[rows_to_practice, 0])
for row in rows_to_practice:
    cur_numpractices = int(vocab_df.loc[row, 'NumPractices'])
    vocab_df.loc[row, 'NextDate'] = config.calculate_next_review(dt.today(), cur_numpractices)
    vocab_df.loc[row, 'NumPractices'] = cur_numpractices + 1
    
vocab_df.to_csv(vocab_file_path, index=False, encoding='utf-8-sig')

ctypes.windll.user32.MessageBoxW(0, '\n'.join(vocab_to_practice), "Practice with These Words!", 0)
