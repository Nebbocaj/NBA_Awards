import pandas as pd

'''
This file add 2023 data onto the datasets
'''


data2023 = pd.read_csv('season2023.csv')


mvp = []
for i in range(len(data2023)):
    mvp.append(0)
data2023["MVP_Votes"] = mvp

data1 = pd.read_csv('NBA_MVP.csv')
data1 = pd.concat([data1, data2023], ignore_index=True, axis = 0)
data1.to_csv('NBA_MVP.csv', index = False)



data2023 = pd.read_csv('season2023.csv')

mvp = []
for i in range(len(data2023)):
    mvp.append(0)
data2023["RotY_Votes"] = mvp

data1 = pd.read_csv('NBA_Rookie.csv')
data1 = pd.concat([data1, data2023], ignore_index=True, axis = 0)
data1.to_csv('NBA_Rookie.csv', index = False)
 



data2023 = pd.read_csv('season2023.csv')

mvp = []
for i in range(len(data2023)):
    mvp.append(0)
data2023["MIP_Votes"] = mvp

data1 = pd.read_csv('NBA_Improved.csv')
data1 = pd.concat([data1, data2023], ignore_index=True, axis = 0)
data1.to_csv('NBA_Improved.csv', index = False)



data2023 = pd.read_csv('season2023.csv')


mvp = []
for i in range(len(data2023)):
    mvp.append(0)
data2023["DPY_Votes"] = mvp

data1 = pd.read_csv('NBA_Defensive.csv')
data1 = pd.concat([data1, data2023], ignore_index=True, axis = 0)
data1.to_csv('NBA_Defensive.csv', index = False)