import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta


#Directories
CSV_DIR = r'C:\My Drive\Firmware Release\EPL Production Test Results\Tests'
#DOWNLOADS_DIR = r'C:\Users\Sakal\Downloads'
DOWNLOADS_DIR = r'C:\Users\sakal.mon\Downloads'

# X-axis labels
X_TICKS = np.arange(0, 1100, 500)

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

    def get_failed(self):
        for file in os.listdir(CSV_DIR):
            print(f'Processing {file}')
            if file.endswith(CEQ_MAP[self.ar][self.line] + '.csv'):
                if get_mdate(file) == todays_date:
                    downloaded_path = copy_to_downloads(file)
                    print(f'File downloaded to {downloaded_path}')

                    self.df = self.df.append(pd.read_csv(downloaded_path, header=2, parse_dates=True), \
                        ignore_index=True)
                    self.df = self.filter_failed()
                        
                    self.count_fails()
                    
                    # Sort counts descending
                    self.fails_count = dict(sorted(self.fails_count.items(), key=lambda item: item[1]))
                    
        return self.fails_count

    def filter_failed(self):
        try:
            filt_failed = self.df['Passed'] == False
            df_failed = self.df.loc[filt_failed]

            df_failed.set_index('Start', inplace=True)
            df_failed.index = pd.to_datetime(df_failed.index)

            for key in self.fails_count.keys():
                df_failed[key] = df_failed[key].astype('bool')

            df_failed_today = df_failed.loc[str(todays_date)]
            return df_failed_today

        except Exception:
            print(f"Error: Can't read dataframe.")

    # Counts the number of different fails
    def count_fails(self):
        for key in self.fails_count.keys():
            if self.df[key].value_counts().shape[0] > 1:
                self.fails_count[key] += self.df[key].value_counts()[0]
            else:
                self.fails_count[key] += 0
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
pd.set_option('display.max_columns', 3)

# Today's date will be used to download result files
todays_date = date.today()

# Initialise enough subplots for 15 lines
fig, ax = plt.subplots(3, 6)

ar2l1 = Results('AR2', 'Line1')
ar2l1_fails = ar2l1.get_failed()
print(ar2l1_fails)

# ax[i,j].barh([key for key in fails_count.keys()], fails_count.values())

# ax[i,j].set_xticks(X_TICKS)
# ax[i,j].title.set_text(f'{ar} - {line}')
# ax[i,j].grid(axis='x')
# reset_counts()

# fig.set_figwidth(15)
# fig.set_figheight(20)
# fig.tight_layout(pad=3.0)
# fig.suptitle('Fails Summary', x=0.53, y=1, fontsize=16)
# plt.grid()
# plt.show()