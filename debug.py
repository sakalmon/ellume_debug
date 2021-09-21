import os
import pandas as pd
import matplotlib.pyplot as plt
import shutil
from datetime import datetime

pd.set_option('display.max_columns', None)
csv_dir = r'C:\My Drive\Firmware Release\EPL Production Test Results\Tests'
downloads_dir = r'C:\Users\Sakal\Downloads'

# For storing number of fails for each test
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
todays_date = datetime.date(datetime.now())

df = pd.DataFrame()

for file in os.listdir(csv_dir):
    if file.endswith(ceq_map[ar][line] + '.csv'):
        file_unix_date = int(os.path.getmtime(os.path.join(csv_dir, file)))
        file_mdate = datetime.date(datetime.fromtimestamp(file_unix_date))

        #if file_mdate == todays_date:
        shutil.copy(os.path.join(csv_dir, file), downloads_dir)
        df = df.append(pd.read_csv(os.path.join(csv_dir, file), header=2))

# Filter for only failed results
filt_failed = df['Passed'] == False

df_failed = df.loc[filt_failed]

# Count number of fails per test
for key in failed_counts.keys():
        try: 
                failed_counts[key] = df[key].value_counts()[0]
        except:
                pass

copy = dict(sorted(failed_counts.items(), key=lambda item: item[1], reverse=True))

# Plot results
plt.bar(range(len(copy)), copy.values(), width=0.5)
plt.xticks(range(len(copy)), copy.keys())
fig = plt.gcf()
fig.set_figwidth(15)
plt.title('Summary of Failures')
plt.ylabel('Occurences')
plt.show()
