import pandas as pd

df = pd.read_csv('./model/alya_open_table.csv')
col_list1 = set(df['cuisine'].tolist())
col_list2 = set(df['location'].tolist())

print(col_list1)
print(col_list2)