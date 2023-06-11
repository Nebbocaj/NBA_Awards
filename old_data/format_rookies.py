import pandas as pd

'''
This program is to combine the NBA_old and NBA_recent datasets from the web into one
dataset called NBA_recent.

Some notes
1. There are multiple columns for some players in the same year.
This is because of a trade. The column where tm ==TOT is the total stats for the year.
Should probbaly focus on that.

2. There is not currently a classification column for awards yet.
This will be done seperately.

3. There is a lot of NaN values in the old data set as not all attributes
were tracked in the 50s. We should probably find a good cut off year to work with
as a lot of NaN values make it harder for a model to learn anything.

'''

#read in data
data = pd.read_csv('NBA_Rookie.csv', encoding='utf-8')
labels = []
for lab in data:
    labels.append(lab)

# df = pd.DataFrame(columns = labels)
# print(df)
# for i in range(len(data)):
#     player = data.iloc[i]
#     test = data.loc[(data['Player'] == player['Player']) & (data['Year'] < player['Year'])]
#     if (len(test) == 0) | (player["RotY_Votes"] > 0):
#         df.loc[len(df.index)] = list(player)
# df = df[df["Year"] >= 1985]
#df.to_csv('NBA_Rookie2.csv', index = False)

#read in data
data = pd.read_csv('NBA_Improved.csv', encoding='utf-8')
data2 = data.drop(['MIP_Votes', 'Pos', 'Tm', 'Year', 'Age', 'Player'], axis = 1)
print(data, data2)
labels = []
for lab in data:
    if lab == 'MIP_Votes':
        break
    labels.append(lab)
    
dup_labels = []
for lab in data2:
    dup_labels.append(lab)
    labels.append(lab + "x")
    
labels.append('MIP_Votes')


df = pd.DataFrame(columns = labels)
print(df)
#Append last year's player data to new year if possible
for i in range(len(data)):
    if i % 100 == 0:
        print(i)
    player = data.iloc[i]
    test = data.loc[(data['Player'] == player['Player']) & (data['Year'] == player['Year'] - 1)]
    ind = data.index[(data['Player'] == player['Player']) & (data['Year'] == player['Year'] - 1)].tolist()
    old = data2.loc[ind]
    if (len(test) != 0):
        p = list(player)
        o = old.values.tolist()[0]
        df.loc[len(df.index)] = p[:-1] + o + [p[-1]]
#%%
print(df)
        
df = df[df["Year"] >= 1985]
df.to_csv('NBA_Improved2.csv', index = False)