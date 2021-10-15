import os
import shutil
import copy
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta

# Disable warnings to hide "SettingWithCopyWarning"
warnings.filterwarnings("ignore")

#Directories
CSV_DIR = r'G:\My Drive\Scientific & Technical\Firmware Release\EPL Production Test Results\Tests'
USER_DIR = os.getenv("USERPROFILE")
DOWNLOADS_DIR = os.path.join(USER_DIR, 'Downloads')

# For locating CEQ number
CEQ_MAP = {
    'AR1': {
        'Line1': 'CEQ0175',
        'Line2': 'CEQ0176',
        'Line3': 'CEQ0271',
        'Line4': 'CEQ0275',
        'Line5': 'CEQ0177',
        'Line6': 'CEQ0179'
    },
    'AR2': {
        'Line1': 'CEQ0178',
        'Line2': 'CEQ0181',
        'Line3': 'CEQ0180',
        'Line4': 'CEQ0192',
        'Line5': 'CEQ0215',
        'Line6': 'CEQ0214'
    },
    'AR3': {
        'Line1': 'CEQ0221',
        'Line2': 'CEQ0212',
        'Line3': 'CEQ0217'
    }
}

class Results:
    def __init__(self, ar, line):
        self.ar = ar
        self.line = line
        self.df = pd.DataFrame()
        self.fails_count = {
            'Firmware Test': 0,                
            'Serial Test': 0,
            'Self-Test Test': 0,
            'Program Test': 0,
            'Batch Test': 0,
            'Bluetooth Test': 0,
            'LED Test': 0,
            'Button Test': 0,
            'Metadata Test': 0,
        }

    def get_failed(self, df):
        for file in os.listdir(CSV_DIR):            
            if file.startswith('6171-ASM') and file.endswith(CEQ_MAP[self.ar][self.line] + '.csv'):
                if get_mdate(file) == todays_date:
                    downloaded_path = copy_to_downloads(file)
                    print(f'File downloaded to {downloaded_path}')
                    
                    if df.index.empty == True:                        
                        df = pd.read_csv(downloaded_path, header=2, parse_dates=True, index_col='Start')
                        if df.empty == True:
                            return
                    
                    else:
                        df = df.append(pd.read_csv(downloaded_path, header=2, parse_dates=True))

                    df = self.filter_failed(df)
                        
                    fails_count = self.count_fails(df, self.fails_count)
                    
                    # Sort counts descending
                    fails_count = dict(sorted(fails_count.items(), key=lambda item: item[1]))

                    return fails_count

    def filter_failed(self, df):
        if df.empty == False:
            filt_failed = df['Passed'] == False
            df_failed = df.loc[filt_failed]

            for key in self.fails_count.keys():
                df_failed[key] = df_failed[key].astype('bool')
            
            try:
                df_failed_today = df_failed.loc[str(todays_date)]
                return df_failed_today
            
            except:
                print('No fails found in this dataframe.')

        else:
            print(f"Error: Can't read dataframe.")
            

    # Counts the number of different fails
    def count_fails(self, df, fails_count):
        for key in self.fails_count.keys():
            if df[key].value_counts().shape[0] > 1:
                fails_count[key] += df[key].value_counts()[0]
            else:
                fails_count[key] += 0

        return fails_count

    def store_counts(self, failed, fails_summary):
        fails_summary[self.ar][self.line] = failed
        
        return fails_summary


# Returns a file's modified date
def get_mdate(file):
    file_unix_date = int(os.path.getmtime(os.path.join(CSV_DIR, file)))
    return date.fromtimestamp(file_unix_date)

# Copies a file from Google drive to the local Downloads folder. Returns file path.
def copy_to_downloads(file):
    file_path = os.path.join(CSV_DIR, file)
    shutil.copy(file_path, DOWNLOADS_DIR)
    return os.path.join(DOWNLOADS_DIR, file)

# Display all columns
pd.set_option('display.max_columns', 10)

# Today's date will be used to download result files
todays_date = date.today()

# Initialise 3 rows for AR and 6 columns for lines
fig, ax = plt.subplots(3, 6, num='Fails Summary')

fails_summary = copy.deepcopy(CEQ_MAP)

for ar, lines in fails_summary.items():
    for line in lines:
        fails_summary[ar][line] = ''

for ar, lines in fails_summary.items():
    for line in lines:
        print(f'Getting results for {ar} {line}...')        
        ar_line = Results(ar, line)
        failed = ar_line.get_failed(ar_line.df)
        fails_summary = ar_line.store_counts(failed, fails_summary)

row_num = 0
col_num = 0

for ar, lines in fails_summary.items():
    for line, fails in lines.items():
        try:
            ax[row_num,col_num].barh(list(fails.keys()), list(fails.values()))
            ax[row_num,col_num].set_yticklabels([key.split(' ')[0] for key in fails.keys()])
            ax[row_num,col_num].title.set_text(f'{ar} - {line}')
        except:
            print(f'No data for {ar} {line}')
            ax[row_num,col_num].axis('off')
        
        ax[row_num,col_num].grid(axis='x')
        
        if col_num < 5:
            col_num += 1
        else:
            col_num = 0
            row_num += 1

        # Disable last three plots as there are only 3 lines in AR3
        for i in range(3, 6):
            ax[2,i].axis('off')

fig.set_figwidth(15)
fig.set_figheight(20)
fig.tight_layout(pad=3.0)
fig.subplots_adjust(hspace=0.5)
plt.show()