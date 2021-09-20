import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


csv_dir = r'C:\My Drive\Firmware Release\EPL Production Test Results\Tests'

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

todays_date = datetime.date(datetime.now())

df = pd.DataFrame()

for file in os.listdir(csv_dir):
    if file.endswith(ceq_map[ar][line] + '.csv'):
        file_unix_date = int(os.path.getmtime(os.path.join(csv_dir, file)))
        file_mdate = datetime.date(datetime.fromtimestamp(file_unix_date))

        if file_mdate == todays_date:
            df = df.append(pd.read_csv(os.path.join(csv_dir, )))

#input()
#     if file.endswith('.csv'):
#         df = df.append(pd.read_csv(file, header=2), ignore_index=True)