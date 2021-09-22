import os
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import pickle
from datetime import date, timedelta

pd.set_option('display.max_columns', None)
csv_dir = r'C:\My Drive\Firmware Release\EPL Production Test Results\Tests'
downloads_dir = r'C:\Users\Sakal\Downloads'

# For storing number of fails for each test
failed_counts = {
        'AR1': {
                'Line1'
        }
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

# For locating CEQ number
ceq_map = {
    'AR1': {'Line1': 'CEQ0175',
            'Line2': 'CEQ0176',
            'Line3': 'CEQ0271',
            'Line4': 'CEQ0275',
            'Line5': 'CEQ0177',
            'Line6': 'CEQ0179'
    },
    'AR2': {'Line1': 'CEQ0178',
            'Line2': 'CEQ0181',
            'Line3': 'CEQ0180',
            'Line4': 'CEQ0192',
            'Line5': 'CEQ0215',
            'Line6': 'CEQ0214'
    },
    'AR3': {'Line1': 'CEQ0221',
            'Line2': 'CEQ0212',
            'Line3': 'CEQ0217'
    }
}

ar = 'AR' + input('AR: ')
line = 'Line' + input('Line: ')


# Today's date will be used to download result files
todays_date = date.today()
#todays_date = date.today().strftime('%Y-%m-%d')

print(todays_date)

df = pd.DataFrame()

for file in os.listdir(csv_dir):
    if file.endswith(ceq_map[ar][line] + '.csv'):
        file_unix_date = int(os.path.getmtime(os.path.join(csv_dir, file)))
        file_mdate = date.fromtimestamp(file_unix_date)

        #if file_mdate == todays_date:
        shutil.copy(os.path.join(csv_dir, file), downloads_dir)
        df = df.append(pd.read_csv(os.path.join(downloads_dir, file), header=3, parse_dates=True), ignore_index=True)

pickle.dump(df, open('df.pickled', 'wb'))

# Filter for only failed results
filt_failed = df['Passed'] == False

df_failed = df.loc[filt_failed]

# Use dates as index
df_failed.set_index('Start', inplace=True)

# Convert dates index to datetime
df_failed.index = pd.to_datetime(df_failed.index)

# Filter for only the current day
try:
        df_failed_today = df_failed.loc[str(todays_date)]

except:
        pass

# Count number of fails per test
for key in failed_counts.keys():
        try: 
                failed_counts[key] = df_failed_today[key].value_counts()[0]
        except:
                pass

# Sort counts descending
failed_counts = dict(sorted(failed_counts.items(), key=lambda item: item[1], reverse=True))

# Plot results
# plt.bar(range(len(failed_counts)), failed_counts.values(), width=0.5)
# plt.xticks(range(len(failed_counts)), failed_counts.keys())
# fig = plt.gcf()
# fig.set_figwidth(15)
# plt.title('Summary of Failures')
# plt.ylabel('Occurences')
# plt.grid(axis='y', linestyle='--')
# plt.show()

fig, (ax1, ax2) = plt.subplots(2)
ax1.bar(range(len(failed_counts)), failed_counts.values(), width=0.5)

yesterdays_date = todays_date - timedelta(days=1)
print(yesterdays_date)

try:
        df_failed_all = df_failed

except:
        pass

# Count number of fails per test
for key in failed_counts.keys():
        try: 
                failed_counts[key] = df_failed_all[key].value_counts()[0]
        except:
                pass

# Sort counts descending
failed_counts = dict(sorted(failed_counts.items(), key=lambda item: item[1], reverse=True))

ax2.bar(range(len(failed_counts)), failed_counts.values(), width=0.5)
fig.set_figwidth(15)
plt.title('Summary of Failures')
plt.show()
