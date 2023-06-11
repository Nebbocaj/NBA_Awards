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
data_old = pd.read_csv('NBA_old.csv').drop('Unnamed: 0', axis = 1)
data_new = pd.read_csv('NBA_recent.csv', encoding='utf-8').drop(["Rk"], axis = 1)


#Get the labels that can be useful.
#NBA_old uses total values for each attribute and NBA_new uses avaerages
#So we need to divide some (not all) attributes by games played.
non_mult = [ "Player", "Pos", "Age", "Tm", "G", "GS", "FG%", "3P%", "2P%", "eFG%", "FT%"]
labels = []
for lab in data_new:
    labels.append(lab)

#Build a new dataframe from NBA_old that matches NBA_recent format
all_rows = []
for i in range(len(data_old)):
    player = data_old.iloc[i]
    games = data_old["G"].iloc[i]
    row = []
    for lab in labels:
        if lab in non_mult:
            try:
                row.append(round(player[lab], 1))
            except:
                row.append(player[lab])
        elif lab in "Year":
            row.append(player[lab])
        else:
            row.append(round(player[lab] / games, 1))
            
    all_rows.append(row)
data_old_mod = pd.DataFrame(all_rows, columns = labels)

#Update the year format in NBA_recent
year_new = []
for y in data_new["Year"]:
    year_new.append(int(y[5:]))
data_new = data_new.drop(['Year'], axis = 1)
data_new['Year'] = year_new

#Combine the two datasets and write them to a csv file to save
data_old_mod = data_old_mod[data_old_mod["Year"] < 1998]
data = pd.concat([data_old_mod, data_new], ignore_index=True, axis = 0)
data.to_csv('NBA_all.csv', index = False)