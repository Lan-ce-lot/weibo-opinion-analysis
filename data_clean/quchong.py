
import pandas as pd
import openpyxl

# 读入excel
df = pd.read_excel('example.xlsx', sheet_name=0)
# print(data)
# 获取表头
head_list = list(df.columns)
print(head_list)


list1 = []
x, y = df.shape
for i in range(x):
    tmp_list = []
    for j in range(y):
        tmp_list.append(df.iloc[i][j])
    list1.append(tmp_list)
print(list1)
for i in range(x):
    print(list1[i])



















