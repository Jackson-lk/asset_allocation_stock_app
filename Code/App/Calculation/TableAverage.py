import pandas as pd
import numpy as np

# Purpose: To average all values in the table based on columns

df_final = pd.read_csv('../../../Dataset/stats_final.csv')
df_final = df_final.drop(['Unnamed: 0'], axis =1 )

header = df_final.columns.values
average = np.delete(header.copy(), 0)

index = 0
for name in header:
    if(name == 'Ticker'):
        pass
    else:
        average[index] = df_final[name].mean()
        index += 1

df_final_mean = df_final.copy()
index = 0
for name in header:
    if(name == 'Ticker'):
        pass
    else:
        # Calculate the average
        for i in range(0, len(df_final.index)):
            df_final_mean.loc[i, name] = (df_final.loc[i, name]/average[index]).round(4)
        index += 1

df_final_mean.to_csv('../../../Dataset/stats_final_mean.csv')



