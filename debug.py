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

#X_TICKS = np.arange(0, 2100, 1000)
X_TICKS = np.arange(0, 1100, 500)
print(X_TICKS)
# Sets the index to time started, converts the time started to datetime object,
# filters and returns a dataframe with only failed results for today.
def get_failed(df):
    try:
        filt_failed = df['Passed'] == False
        df_failed = df.loc[filt_failed]

        df_failed.set_index('Start', inplace=True)
        df_failed.index = pd.to_datetime(df_failed.index)

        for key in fails_count.keys():
            df_failed[key] = df_failed[key].astype('bool')

        df_failed_today = df_failed.loc[str(todays_date)]
        return df_failed_today

    except Exception:
        print(f"Error: Can't read dataframe.")

# Reset and return a dictionary for counting the number of different fails
def reset_counts():
    global fails_count
    fails_count = {
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

# Get room and line number
def get_input():
    ar = 'AR' + input('AR: ')
    line = 'Line' + input('Line: ')

    return (ar, line)


# Returns a file's modified date
def get_mdate(file):
    file_unix_date = int(os.path.getmtime(os.path.join(CSV_DIR, file)))
    return date.fromtimestamp(file_unix_date)

# Copies a file from Google drive to the local Downloads folder. Returns file path.
def copy_to_downloads(file):
    file_path = os.path.join(CSV_DIR, file)
    shutil.copy(file_path, DOWNLOADS_DIR)
    return os.path.join(DOWNLOADS_DIR, file)

# Counts the number of different fails
def count_fails(df):
    try:
        for key in fails_count.keys():
            fails_count[key] = df[key].value_counts()[0]
    except Exception:
        print(f'Error: Unable to count fails.')

# Today's date will be used to download result files
todays_date = date.today()

# Display all columns
pd.set_option('display.max_columns', 3)

#ar, line = get_input()

# Initialise subplots for 12 lines
fig, ax = plt.subplots(3, 6)

#ar, line = get_input()

# For counting number of plots
i = 0
j = -1

fails_count = {
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

# Initialise dictionary for storing fails
reset_counts()
print(f'keys: {[key for key in fails_count.keys()]}')
for file in os.listdir(CSV_DIR):
    print(f'Processing {file}')
    for ar, lines in CEQ_MAP.items():
        for line, ceq in lines.items():
            if file.endswith(ceq + '.csv'):
                file_mdate = get_mdate(file)
                print(f"File's Modified Date: {file_mdate}")
                if file_mdate == todays_date:
                    downloaded_path = copy_to_downloads(file)
                    print(f'File downloaded to {downloaded_path}')

                
                    df = pd.read_csv(downloaded_path, header=2, parse_dates=True)
                    df_failed_today = get_failed(df)
                    
                    count_fails(df_failed_today)
                
                    # Sort counts descending
                    fails_count = dict(sorted(fails_count.items(), key=lambda item: item[1]))
                    

                    if j == 5:
                        i += 1
                        j = 0
                    else:
                        j += 1

                    # ax[i,j].bar(range(len(fails_count)), fails_count.values(), width=0.5)
                    ax[i,j].barh([key for key in fails_count.keys()], fails_count.values())
                    #ax[i,j].set_xticks(np.arange(len(fails_count.keys())))
                    #ax[i,j].set_xticklabels([key.split(' ')[0] for key in fails_count.keys()], rotation=70)
                    ax[i,j].set_xticks(X_TICKS)
                    ax[i,j].title.set_text(f'{ar} - {line}')
                    ax[i,j].grid(axis='x')
                    reset_counts()

#ax.set_xticks(range(len(fails_count)), fails_count.keys())

#ax.set_xticklabels(fails_count.keys())
fig.set_figwidth(15)
fig.set_figheight(20)
fig.tight_layout(pad=3.0)
fig.suptitle('Fails Summary', x=0.53, y=1, fontsize=16)
plt.grid()
plt.show()

# Plot results
# plt.bar(range(len(failed_counts)), failed_counts.values(), width=0.5)
# plt.xticks(range(len(failed_counts)), failed_counts.keys())
# fig = plt.gcf()
# fig.set_figwidth(15)
# plt.title('Summary of Failures')
# plt.ylabel('Occurences')
# plt.grid(axis='y', linestyle='--')
# plt.show()