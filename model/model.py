import os
import ml_utils as mlu
import pandas as pd
from sklearn.model_selection import train_test_split

os.chdir(os.path.join(os.path.dirname(os.path.realpath('__file__')),'../data'))
print(os.getcwd())

dfs = [pd.read_csv(f, index_col=[0], parse_dates=[0])
        for f in os.listdir(os.getcwd()) if f.endswith('csv')]

final_df = pd.concat(dfs, axis=1, join='inner').sort_index()

#os.remove('out.csv')

final_df.to_csv('out.csv')

#mlu.print_dataframe_summary(final_df)
y = final_df['gold_price']
X = final_df.drop('gold_price',  axis=1)


print(X.head())
print(y.head())

# Load and split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

mlu.model_comparison(X_train, X_test, y_train, y_test)