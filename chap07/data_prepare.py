import pandas as pd

red_df = pd.read_csv('wine+quality/winequality-red.csv', sep=';', header=0, engine='python')
white_df = pd.read_csv('wine+quality/winequality-white.csv', sep=';', header=0, engine='python')

red_df.to_csv('wine+quality/winequality-red2.csv', index=False)
white_df.to_csv('wine+quality/winequality-white2.csv', index=False)
