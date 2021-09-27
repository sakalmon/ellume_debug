import os
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import pickle
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

# Sets the index to time started, converts the time started to datetime object,
# filters and returns a dataframe with only failed results for today.
def get_failed(df):
    filt_failed = df['Passed'] == False
    df_failed = df.loc[filt_failed]
    df_failed.set_index('Start', inplace=True)
    df_failed.index = pd.to_datetime(df_failed.index)

    try:
        df_failed_today = df_failed.loc[str(todays_date)]
        return df_failed_today
    except:
        pass

# Reset and return a dictionary for counting the number of different fails
def reset_counts():
    failed_counts = {
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
    return failed_counts

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
def count_fails(df, counts_dict):
    for key in counts_dict.keys():
        try: 
            counts_dict[key] = df[key].value_counts()[0]
            return counts_dict
        except:
            return reset_counts()

# Display all columns
pd.set_option('display.max_columns', None)

# Today's date will be used to download result files
todays_date = date.today()

#ar, line = get_input()

# Initialise subplots for 12 lines
fig, ax = plt.subplots(1)

#ar, line = get_input()

# For counting number of plots
i = 1

# Initialise dictionary for storing fails
failed_counts = reset_counts()

for file in os.listdir(CSV_DIR):
    for ar, lines in CEQ_MAP.items():
        for line, ceq in lines.items():
            if file.endswith(ceq + '.csv'):
                file_mdate = get_mdate(file)

                #if file_mdate == todays_date:
                downloaded_path = copy_to_downloads(file)

                try:
                    df = pd.read_csv(downloaded_path, header=2, parse_dates=True)
                    df_failed_today = get_failed(df)
                    fails_count = count_fails(df_failed_today, failed_counts)
                    # Sort counts descending
                    fails_count = dict(sorted(fails_count.items(), key=lambda item: item[1], reverse=True))
                except:
                    pass

            
            ax.bar(range(len(fails_count)), fails_count.values(), width=0.5)           

            failed_counts = reset_counts()
            i += 1

ax.set_ticks(range(len(fails_count)), fails_count.keys())
fig.set_figwidth(15)
plt.title('Summary of Failures')
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