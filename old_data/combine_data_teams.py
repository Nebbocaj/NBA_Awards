import pandas as pd

'''
This file cleans the data, removes duplicates, and adds a win% column to the data.
'''

data = pd.read_csv('NBA_all.csv')
team_data = pd.read_csv('Team_Records.csv')


#Remove all data from players before 1981 as there is limited info before then
data = data[data["Year"] >= 1981]
team_data = team_data[team_data["Season"] >= 1981]

win_per = []

for index, row in data.iterrows():
    
    vals = team_data.index[(team_data['Season'] == row["Year"]) & (team_data["Team"] == row["Tm"])].tolist()
    
    if len(vals) > 0:
        wins = float(team_data.loc[vals]["W/L%"])
    else:
        wins = 0.5
    win_per.append(wins)
    
data["Win%"] = win_per 

data.to_csv('NBA_all_wins.csv', index = False)

#Remove unneeded indicator in player names
for index, row in data.iterrows():
    player = data.loc[index]["Player"]
    if player[-1]  == '*':
        data.at[index, "Player"] = player[:-1]
        


#remove all duplicate when player were traded
dups = data[data["Tm"] == "TOT"]
extras = []
for index, row in dups.iterrows():
    vals = data.index[(data['Player'] == row["Player"]) & (data["Year"] == row["Year"])].tolist()
    vals = vals[:-1]
    extras += vals
    
data = data.drop(extras)

data.to_csv('NBA_all_cleaned.csv', index = False)

#%%

#Add the label with MVP voting
mvp_data = pd.read_csv('rookie_of_the_year_data.csv', encoding='latin-1')
mvp = []
for index, row in data.iterrows():
    vals = mvp_data.index[(mvp_data['Player'] == row["Player"]) & (mvp_data["Year"] == row["Year"])].tolist()
    if len(vals) > 0:
        
        #Total used in getting percentage of votes
        total_points = sum(mvp_data[mvp_data["Year"] == row["Year"]]["Pts Won"].tolist())
        mvp.append(round(mvp_data.loc[vals]["Pts Won"].tolist()[0] / total_points,4))
        
    else:
        mvp.append(0)
data["RotY_Votes"] = mvp

data = data[data["Year"] >= 1981]
 
data.to_csv('NBA_Rookie.csv', index = False)
        