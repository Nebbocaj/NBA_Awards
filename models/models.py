import os
os.environ['R_HOME'] = 'C:\Program Files\R\R-4.3.0' #CHANGE THIS TO THE R LOCATION OF YOUR DEVICE

from rpy2 import robjects

import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import MaxAbsScaler

robjects.r('''
    MVP_model <- function() {
        

        library("caret")
        library("caretEnsemble")
        
        mdl <- readRDS("MVP_mdl.rds")
        
        data <- read.csv("test_data.csv")
        
        t <- predict(mdl, data)
        
        return(t)
    }
    
    DEF_model <- function() {
        

        library("caret")
        library("caretEnsemble")
        
        mdl <- readRDS("DEF_mdl.rds")
        
        data <- read.csv("test_data.csv")
        
        t <- predict(mdl, data)
        
        return(t)
    }
    
    IMP_model <- function() {
        

        library("caret")
        library("caretEnsemble")
        
        mdl <- readRDS("IMP_mdl.rds")
        
        data <- read.csv("test_data.csv")
        
        t <- predict(mdl, data)
        
        return(t)
    }
    
    Rookie_model <- function() {
        

        library("caret")
        library("caretEnsemble")
        library("RSNNS")
        
        mdl <- readRDS("Rookie_mdl.rds")
        
        data <- read.csv("test_data.csv")
        
        t <- predict(mdl, data)
        
        return(t)
    }
''')

def get_predictions(award = "MVP", season = 2023, pred_num = 3):
    print(f'{award}+{season}+{pred_num}')
    if (season < 2000) | (season > 2023):
        return
    
    if (pred_num < 1) | (pred_num > 10):
        return
    
    #change path directory according to your local    
    if award == "MVP":
        #read in data and drop useless columns
        df = pd.read_csv('NBA_MVP.csv', encoding='utf-8')
        df = df[df["Year"] >= 1982]
        df = df.drop(columns = ['Pos', 'Tm'])
        
        #Fill all null values with zero as all null values in the data are
        #from 0/0 percentages.
        df = df.fillna(0)
        df = df.reset_index()
        
        #Split data into train and test sets.
        train = df[df["Year"] < season].drop(columns = ['Year']).reset_index()
        test = df[df["Year"] == season].drop(columns = ['Year']).reset_index()
        
        train_data2 = train.drop(columns = ['MVP_Votes', 'index'])
        train_data = train_data2.drop(columns = ['Player', 'level_0'])
        test_label = test["MVP_Votes"]
        test_data2 = test.drop(columns = ['MVP_Votes', 'index'])
        test_data = test_data2.drop(columns = ['Player', 'level_0'])
        
        cleaned = df.drop(columns = ['Year', 'Player', 'MVP_Votes', 'index'])
        label = df["MVP_Votes"]

        
    elif award == "DPY":
        #read in data and drop useless columns
        df = pd.read_csv('NBA_Defensive.csv', encoding='utf-8')
        df = df[df["Year"] >= 1982]
        df = df.drop(columns = ['Pos', 'Tm'])
        
        #Fill all null values with zero as all null values in the data are
        #from 0/0 percentages.
        df = df.fillna(0)
        df = df.reset_index()
        
        #Split data into train and test sets.
        train = df[df["Year"] < season].drop(columns = ['Year']).reset_index()
        test = df[df["Year"] == season].drop(columns = ['Year']).reset_index()
        
        train_data2 = train.drop(columns = ['DPY_Votes', 'index'])
        train_data = train_data2.drop(columns = ['Player', 'level_0'])
        test_label = test["DPY_Votes"]
        test_data2 = test.drop(columns = ['DPY_Votes', 'index'])
        test_data = test_data2.drop(columns = ['Player', 'level_0'])
        
        cleaned = df.drop(columns = ['DPY_Votes', 'Year', 'Player', 'index'])
        label = df["DPY_Votes"]
        
    elif award == "RotY":
        #read in data and drop useless columns
        df = pd.read_csv('NBA_Rookie.csv', encoding='utf-8')
        df = df[df["Year"] >= 1982]
        df = df.drop(columns = ['Pos', 'Tm'])
        
        #Fill all null values with zero as all null values in the data are
        #from 0/0 percentages.
        df = df.fillna(0)
        df = df.reset_index()
        
        #Split data into train and test sets.
        train = df[df["Year"] < season].drop(columns = ['Year']).reset_index()
        test = df[df["Year"] == season].drop(columns = ['Year']).reset_index()
        
        train_data2 = train.drop(columns = ['RotY_Votes', 'index'])
        train_data = train_data2.drop(columns = ['Player', 'level_0'])
        test_label = test["RotY_Votes"]
        test_data2 = test.drop(columns = ['RotY_Votes', 'index'])
        test_data = test_data2.drop(columns = ['Player', 'level_0'])
        
        cleaned = df.drop(columns = ['RotY_Votes', 'Year', 'Player', 'index'])
        label = df["RotY_Votes"]
        
    elif award == "MIP":
        #read in data and drop useless columns
        df = pd.read_csv('NBA_Improved2.csv', encoding='utf-8')
        df = df[df["Year"] >= 1982]
        df = df.drop(columns = ['Pos', 'Tm'])
        
        #Fill all null values with zero as all null values in the data are
        #from 0/0 percentages.
        df = df.fillna(0)
        df = df.reset_index()
        
        #Split data into train and test sets.
        train = df[df["Year"] < season].drop(columns = ['Year']).reset_index()
        test = df[df["Year"] == season].drop(columns = ['Year']).reset_index()
        
        train_data2 = train.drop(columns = ['MIP_Votes', 'index'])
        train_data = train_data2.drop(columns = ['Player', 'level_0'])
        test_label = test["MIP_Votes"]
        test_data2 = test.drop(columns = ['MIP_Votes', 'index'])
        test_data = test_data2.drop(columns = ['Player', 'level_0'])
        
        cleaned = df.drop(columns = ['MIP_Votes', 'Year', 'Player', 'index'])
        label = df["MIP_Votes"]
        
    else:
        return 0
    
    #Normalize data
    
    train_data = pd.DataFrame(MaxAbsScaler().fit(train_data).transform(train_data))
    test_data = pd.DataFrame(MaxAbsScaler().fit(test_data).transform(test_data))
    cleaned = pd.DataFrame(MaxAbsScaler().fit(cleaned).transform(cleaned))
    cleaned["Votes"] = label
    
    cleaned = cleaned.rename(columns={0: 'Age', 1: 'G', 2: 'GS', 3: 'MP', 4: 'FG', 5: 'FGA'
                                      , 6:'FG%', 7:'3P', 8:'3PA', 9:'3P%', 10:'2P', 11:'2PA', 12:'2P%',
                                      13:'eFG%', 14:'FT', 15:'FTA', 16:'FT%', 17:'ORB', 18:'DRB',
                                      19:'TRB',20:'AST', 21:'STL', 22:'BLK', 23:'TOV', 24:'PF', 25:'PTS', 26:'Win%'})
    
    test_data = test_data.rename(columns={0: 'Age', 1: 'G', 2: 'GS', 3: 'MP', 4: 'FG', 5: 'FGA'
                                      , 6:'FG%', 7:'3P', 8:'3PA', 9:'3P%', 10:'2P', 11:'2PA', 12:'2P%',
                                      13:'eFG%', 14:'FT', 15:'FTA', 16:'FT%', 17:'ORB', 18:'DRB',
                                      19:'TRB',20:'AST', 21:'STL', 22:'BLK', 23:'TOV', 24:'PF', 25:'PTS', 26:'Win%'})
    
    train_data = train_data.rename(columns={0: 'Age', 1: 'G', 2: 'GS', 3: 'MP', 4: 'FG', 5: 'FGA'
                                      , 6:'FG%', 7:'3P', 8:'3PA', 9:'3P%', 10:'2P', 11:'2PA', 12:'2P%',
                                      13:'eFG%', 14:'FT', 15:'FTA', 16:'FT%', 17:'ORB', 18:'DRB',
                                      19:'TRB',20:'AST', 21:'STL', 22:'BLK', 23:'TOV', 24:'PF', 25:'PTS', 26:'Win%'})
    test_data.to_csv('test_data.csv', index = False)
    
    if award == "MVP":
        model = robjects.r['MVP_model']
        
    elif award == "DPY":
        model = robjects.r['DEF_model']
        
    elif award == "RotY":
        model = robjects.r['Rookie_model']
        
    elif award == "MIP":
        model = robjects.r['IMP_model']
    
    predict = np.asarray(model())
    
    #get top 10 predictions and actual winners
    ordered = np.argsort(predict)[::-1][:11]
    actual = np.argsort(test_label.to_numpy())[::-1][:11]
    
    #Convert the predicted data into percentages
    percentage = []
    for i in range(len(ordered) - 1):
        percentage.append(predict[ordered[i]] - predict[ordered[10]])
    percentage = percentage / sum(percentage)
    
    #Get the predicted player
    predicted_players = []
    for i in range(min(pred_num,len(ordered) - 1) ):
        player = test_data2.at[ordered[i],'Player']
        predicted_players.append([player, round(percentage[i],4)])
        
    #get the actual winners
    actual_players = []
    for i in range(min(pred_num,len(ordered) - 1) ):
        if season == 2023:
            player = "?"
        else:
            player = test_data2.at[actual[i],'Player']
        actual_players.append([player, test_label[actual[i]]])
        
        
    cleaned.to_csv('NBA_Rookie_clean.csv', index = False)

    return predicted_players, actual_players

def jaccard(set1, set2):
    count = 0
    for elem in set1:
        if elem in set2:
            count += 1
    return count / len(set1)
 
    
def score(set1, set2):
    
    final = 0
    count1 = 0
    for i in range(1,len(set2)+1)[::-1]:
        s = i
        p = 4
        player1 = set1[count1]
        count2 = 0
        for j in range(1,len(set1)+1)[::-1]:
            player2 = set2[count2]
            count2 += 1
            if player1 == player2:
                p = j
                break
        count1 += 1
        
        
        final += (s-p)**2
    
    return math.sqrt(final)/6
size = 10

total_J = []
total_S = []
y1 = 2000
y2 = 2023
for y in range(y1, y2):
    pred, act = get_predictions("MVP", y, size)
        
    for o in range(size):
        print(pred[o], act[o]) 
        
    pred_vals = [pred[i][0] for i in range(size)]
    act_vals = [act[i][0] for i in range(size)]
    
    J = jaccard(pred_vals, act_vals)
    S = score(pred_vals[:3], act_vals[:3])
    print(J, S)
    
    total_J.append(J)
    total_S.append(round(S, 2))
    
print("Average Jaccard: ", sum(total_J) / len(total_J), np.std(total_J),)
print("Average Score: ", sum(total_S) / len(total_S), np.std(total_S), total_S)

