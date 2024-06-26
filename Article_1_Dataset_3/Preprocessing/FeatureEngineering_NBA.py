#Importing necessary libraries and modules.
import warnings
import numpy as np
import pandas as pd 
from collections import OrderedDict
from InputData import loadDataFrameList

warnings.filterwarnings('ignore')

## Loading the list of dataframes from DataPreprocessing.
DataFrames = loadDataFrameList()

print(DataFrames[0]["Season"])

print(DataFrames[2].head(5))

a = 5

'''-----------------------------------     Adding Goal Difference as a Feature  --------------------------------------------'''
## Creating a function that computes the columns "home_team_total_position_difference" and "away_team_total_position_difference"  
def computeTGD(DataFrame) :
    
    ## Initialising the values contained in the coloumns "home_team_total_position_difference" and "away_team_total_position_difference" 
    DataFrame['home_team_total_position_difference'] = np.nan
    DataFrame['away_team_total_position_difference'] = np.nan
    
    ## Creating a list of all the teams that played in that season .
    Teams = list((DataFrame).home_team.unique())

    number_teams = len(Teams)

    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise .
    for z in range(0, number_teams):

        matches_played = ((DataFrame['home_team'] == Teams[z]) | (DataFrame['away_team'] == Teams[z])).sum()

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[ (DataFrame['home_team'] == str(Teams[z]) ) | ( DataFrame['away_team'] == str(Teams[z])) ]

        ## Creating a list which contains "Matchwise Goal Difference" for the team under observation .
        MGDList = []

        for index, row in tempDF.iterrows():

            if (Teams[z] == row['home_team']):
                MGDList.append(row['match_hometeam_position_difference'])

            elif (Teams[z] == row['away_team']):
                MGDList.append(row['match_awayteam_position_difference'])

        ## Creating a list which contains "Goal Difference" for the team under observation before coming into each match.
        GDList = []

        for i in range(0, matches_played):
            
            ## When the team has played no match.
            if (i == 0):
                GDList.append(0)
            
            ## When the team has played exactly one match.
            elif (i == 1):
                GDList.append(MGDList[i - 1])
            
            ## When the team has played more than 1 match.
            else:
                GDList.append(GDList[i - 1] + MGDList[i - 1])


        ## We will now normalise the Goal Difference.
        for m in range(0, matches_played):

            GDList[m] /= 100

        ## Creating a list for the index values of the games contained in tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.

        indexHome = []
        indexAway = []

        for index, row in tempDF.iterrows():
            
            ## If team was Home Team.
            if (Teams[z] == row['home_team']):
                 indexHome.append(index)
                    
            ## If team was Away Team.
            elif (Teams[z] == row['away_team']):
                indexAway.append(index)

        ## Appending the appropriate "Goal Difference" values to the dataframe .
        for j in range(0, matches_played):

            if (gameIndices[j] in indexHome):
                DataFrame['home_team_total_position_difference'][gameIndices[j]] = GDList[j]
            elif (gameIndices[j] in indexAway):
                DataFrame['away_team_total_position_difference'][gameIndices[j]] = GDList[j]

    ## Filling in the columns for "GD".
    DataFrame['home_away_total_position_differential'] = DataFrame.apply(lambda row: row['home_team_total_position_difference'] - row['away_team_total_position_difference'], axis = 1)


''''-----------------------------------     Adding KPP as a Feature  --------------------------------------------'''

## Creating a function which computes the KPP (K-Past Performance) feature for Points, Assists and Free Throws .

def computeKPP(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).HOME_TEAM_ID.unique())

    number_teams = len(Teams)
    
    ## Initialising the values contained in the coloumns "HGKPP , HCKPP , HSTKPP" and "AGKPP , ACKPP , ASTKPP". (KPP Features).
    DataFrame['k_past_points_home'] = np.nan
    DataFrame['k_past_assists_home'] = np.nan
    DataFrame['k_past_rebounds_home'] = np.nan

    DataFrame['k_past_points_away'] = np.nan
    DataFrame['k_past_assists_away'] = np.nan
    DataFrame['k_past_rebounds_away'] = np.nan

    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, number_teams):

        matches_played = ((DataFrame['HOME_TEAM_ID'] == Teams[z]) | (DataFrame['VISITOR_TEAM_ID'] == Teams[z])).sum()

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['HOME_TEAM_ID'] == Teams[z]) | ( DataFrame['VISITOR_TEAM_ID'] == Teams[z])]

        ## Creating a list which contains Goals, Corners and Number of Shots on Target for the team under observation match-wise.
        Points = []
        Assists = []
        Rebounds = []

        for index, row in tempDF.iterrows():
    
            if (Teams[z] == row['HOME_TEAM_ID']):
                Points.append(float(row['PTS_home']))
                Assists.append(float(row['AST_home']))
                Rebounds.append(float(row['REB_home']))

            elif (Teams[z] == row['VISITOR_TEAM_ID']):
                Points.append(float(row['PTS_away']))
                Assists.append(float(row['AST_away']))
                Rebounds.append(float(row['REB_away']))

        ## Creating lists to hold values for the corresponding KPP Features.
        # Since these features will be non existent for the first k matches of each team, fill Nan for the first k values.
        pointsKPP = [np.nan] * k
        assistsKPP = [np.nan] * k
        reboundsKPP = [np.nan] * k

        ## Adding appropriate values to the list.
        ## The number of computations performed will be (n + 1 - k) where :
        ## n = number of matches in the season for each team (38).
        ## k = sliding window hyper-parameter.
        for i in range(0, (matches_played + 1 - k)):

            ## Obtaining the slice of records to be observed.
            ## Sum the slice of records and normalize it by k.
            pointsSliceSum = sum(Points[i : (i + k)])/k
            assistsSliceSum = sum(Assists[i : (i + k)])/k
            reboundsSliceSum = sum(Rebounds[i : (i + k)])/k

            ## Appending to the list of the corresponding KPP features.
            pointsKPP.append(pointsSliceSum)
            assistsKPP.append(assistsSliceSum)
            reboundsKPP.append(reboundsSliceSum)
            
        ## Creating a list for the index values of the games contained in the tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.
        indexHome = []
        indexAway = []

        ## Segregate home and away match indices.
        for index, row in tempDF.iterrows():
            
            if (Teams[z] == row['HOME_TEAM_ID']):
                 indexHome.append(index)

            elif (Teams[z] == row['VISITOR_TEAM_ID']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the dataframe.
        for j in range(0, matches_played):

            if (gameIndices[j] in indexHome):
                DataFrame['k_past_points_home'][gameIndices[j]] = pointsKPP[j]
                DataFrame['k_past_assists_home'][gameIndices[j]] = assistsKPP[j]
                DataFrame['k_past_rebounds_home'][gameIndices[j]] = reboundsKPP[j]

            elif (gameIndices[j] in indexAway):
                DataFrame['k_past_points_away'][gameIndices[j]] = pointsKPP[j]
                DataFrame['k_past_assists_away'][gameIndices[j]] = assistsKPP[j]
                DataFrame['k_past_rebounds_away'][gameIndices[j]] = reboundsKPP[j]
        
    ## Filling in the coloumns for "GKPP, CKPP, STKPP".
    DataFrame['k_past_points_diff'] = DataFrame.apply(lambda row: row['k_past_points_home'] - row['k_past_points_away'], axis = 1)
    DataFrame['k_past_assists_diff'] = DataFrame.apply(lambda row: row['k_past_assists_home'] - row['k_past_assists_away'], axis = 1)
    DataFrame['k_past_rebounds_diff'] = DataFrame.apply(lambda row: row['k_past_rebounds_home'] - row['k_past_rebounds_away'], axis = 1)

''''-----------------------------------     Adding Streak and Weighted Streak as a Feature  --------------------------------------------'''

## Creating a function which computes the Streak and Weighted Streak

def computeStreak(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).HOME_TEAM_ID.unique())

    number_teams = len(Teams)
    
    ## Initialsing the values in the coloumns "HSt, ASt , HStWeigted , AStWeigted".
    DataFrame['Home_St'] = np.nan
    DataFrame['Away_St'] = np.nan
    DataFrame['Home_StWeighted'] = np.nan
    DataFrame['Away_StWeighted'] = np.nan
    
    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, number_teams):

        matches_played = ((DataFrame['HOME_TEAM_ID'] == Teams[z]) | (DataFrame['VISITOR_TEAM_ID'] == Teams[z])).sum()

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['HOME_TEAM_ID'] == Teams[z]) | ( DataFrame['VISITOR_TEAM_ID'] == Teams[z])]
    
        ## Creating a list which contains the points assigned to each team after their match. 
        ## 0 - Loss
        ## 1 - Draw
        ## 3 - Win
        matchPoints = []

        ## Creating a list which contains the weights assigned to each match according to the sliding window hyper-parameter.
        ## The weighting scheme is such that the first match in the window will be a assigned a weight of 1 and the last match will be 
        ## assigned a weight of k.
        weightList = [(i + 1) for i in range(0, k)]
        
        for index , row in tempDF.iterrows():
            
            if (Teams[z] == row['HOME_TEAM_ID']):
                if (row['HOME_TEAM_WINS'] == 1) :
                    matchPoints.append(3.0)
                elif (row['HOME_TEAM_WINS'] == 0) :
                    matchPoints.append(0)

            elif (Teams[z] == row['VISITOR_TEAM_ID']):
                if (row['HOME_TEAM_WINS'] == 1) :
                    matchPoints.append(0.0)
                elif (row['HOME_TEAM_WINS'] == 0) :
                    matchPoints.append(3.0)
 
        ## Creating lists to hold values for the corresponding Streak and Weighted Streak Features.
        ## Since these features will be non existent for the first k matches of each team, fill Nan for the first k values.
        streak = [np.nan] * k
        weightedStreak = [np.nan] * k
        
        ## Adding appropriate values to the list.
        ## The number of computations performed will be (n + 1 - k) where :
        ## n = number of matches in the season for each team (38).
        ## k = sliding window hyper-parameter.
        for i in range(0, (matches_played + 1 - k)):

            ## Obtaining the slice of records to be observed.
            matchPointsSlice = matchPoints[i : (i + k)]

            ## Sum the slice of records and normalize it by 3k.
            streakValue = sum(matchPointsSlice)/(3 * k)

            ## Multiply the slice by the weights.
            ## Sum the slice of records and normalize it by (3k(k+1))/2.
            weightedStreakValue = sum(list(np.array(matchPointsSlice) * np.array(weightList)))/((1.5) * k * (k + 1))

            ## Appending to the list of the corresponding features.
            streak.append(streakValue)
            weightedStreak.append(weightedStreakValue)
            
        ## Creating a list for the index values of the games contained in the tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.
        indexHome = []
        indexAway = []

        ## Segregate home and away match indices.
        for index, row in tempDF.iterrows():

            if (Teams[z] == row['HOME_TEAM_ID']):
                 indexHome.append(index)

            elif (Teams[z] == row['VISITOR_TEAM_ID']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the dataframe.
        for j in range(0, matches_played):

            if (gameIndices[j] in indexHome):
                DataFrame['Home_St'][gameIndices[j]] = streak[j]
                DataFrame['Home_StWeighted'][gameIndices[j]] = weightedStreak[j]

            elif (gameIndices[j] in indexAway):
                DataFrame['Away_St'][gameIndices[j]] = streak[j]
                DataFrame['Away_StWeighted'][gameIndices[j]] = weightedStreak[j]
                
    ## Filling in the coloumns for "Streak and WeightedStreak".
    DataFrame['Streak'] = DataFrame.apply(lambda row: row['Home_St'] - row['Away_St'], axis = 1)
    DataFrame['WeightedStreak'] = DataFrame.apply(lambda row: row['Home_StWeighted'] - row['Away_StWeighted'], axis = 1)

''''-----------------------------------     Adding Form as a Feature  --------------------------------------------'''

## Creating a function which computes the Form.

def computeForm(DataFrame, stealingFraction):
    
    ## Hyper-Parameter k.
    k = stealingFraction

    ## Initialising the values contained in the coloumns "HForm" and "AForm".
    DataFrame['HForm'] = 1.0
    DataFrame['AForm'] = 1.0

    ## Creating a global form dictionary with keys as team names and value as list of form.
    gFormDict = {}

    ## Creating a global form dictionary with keys as team names and value as list of match indices.
    teamMatchLookup = {}

    ## Dictionary which keeps track of a team's match indices.
    matchCounterDict = {}

    ## Creating a list of all the teams that played in that season .
    Teams = list((DataFrame).HOME_TEAM_ID.unique())

    for teamName in Teams :

        ## Initialising values.
        gFormDict[teamName] = 1.0
        matchCounterDict[teamName] = 0

        ## For each team playing in the season, create a temporary dataframe to record the match numbers of each team.
        ## Create a temporary dataframe for the team under consideration.
        tempDF = DataFrame[(DataFrame['HOME_TEAM_ID'] == str(teamName)) | ( DataFrame['VISITOR_TEAM_ID'] == str(teamName))]

        ## Assigning match indices list to the relevant team.
        teamMatchLookup[teamName] =  tempDF.index.tolist()

    ## Iterating over each match in the season.
    for index, row in DataFrame.iterrows():
        
        ## Exit condition. Since the last update in the form values will be in the 2nd last match for each team, we have to run the loop till each team's 2nd last match.
        ## This condition happens at the 370th in each season.
        if (index == 370):
        
            break

        ## Update match counter for the playing teams.
        matchCounterDict[row['HOME_TEAM_ID']] += 1
        matchCounterDict[row['VISITOR_TEAM_ID']] += 1

        ## Case where home team wins. Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team.        
        if (row['HOME_TEAM_WINS'] == '1'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['HOME_TEAM_ID']]
            prevAwayForm = gFormDict[row['VISITOR_TEAM_ID']]

            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['HOME_TEAM_ID']][matchCounterDict[row['HOME_TEAM_ID']]]
            nextMatchA = teamMatchLookup[row['VISITOR_TEAM_ID']][matchCounterDict[row['VISITOR_TEAM_ID']]]
    
            ## Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team. 
            homeUpdate = gFormDict[row['HOME_TEAM_ID']] + k * gFormDict[row['VISITOR_TEAM_ID']]
            awayUpdate = gFormDict[row['VISITOR_TEAM_ID']] - k * gFormDict[row['HOME_TEAM_ID']]

            ## Selecting next match record for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['HOME_TEAM_ID'][nextMatchH] == row['HOME_TEAM_ID']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['VISITOR_TEAM_ID'][nextMatchH] == row['HOME_TEAM_ID']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['HOME_TEAM_ID']] = homeUpdate

            ## Selecting next match record for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['HOME_TEAM_ID'][nextMatchA] == row['VISITOR_TEAM_ID']):
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['VISITOR_TEAM_ID'][nextMatchA] == row['VISITOR_TEAM_ID']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['VISITOR_TEAM_ID']] = awayUpdate


        ## Case where away team wins. Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
        if (row['HOME_TEAM_WINS'] == '0'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['HOME_TEAM_ID']]
            prevAwayForm = gFormDict[row['VISITOR_TEAM_ID']]
        
            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['HOME_TEAM_ID']][matchCounterDict[row['HOME_TEAM_ID']]]
            nextMatchA = teamMatchLookup[row['VISITOR_TEAM_ID']][matchCounterDict[row['VISITOR_TEAM_ID']]]

            ## Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
            homeUpdate = gFormDict[row['HOME_TEAM_ID']] - k * gFormDict[row['VISITOR_TEAM_ID']]
            awayUpdate = gFormDict[row['VISITOR_TEAM_ID']] + k * gFormDict[row['HOME_TEAM_ID']]

            ## Selecting next match for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['HOME_TEAM_ID'][nextMatchH] == row['HOME_TEAM_ID']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AWAY_TEAM_ID'][nextMatchH] == row['HOME_TEAM_ID']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['HOME_TEAM_ID']] = homeUpdate

            ## Selecting next match for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['HOME_TEAM_ID'][nextMatchA] == row['VISITOR_TEAM_ID']):            
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['VISITOR_TEAM_ID'][nextMatchA] == row['VISITOR_TEAM_ID']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['VISITOR_TEAM_ID']] = awayUpdate
    
    # Filling in the coloumns for "Form".
    DataFrame['Form'] = DataFrame.apply(lambda row: row['HForm'] - row['AForm'], axis = 1)

## Computing features for all the data.
for i, dataFrame in enumerate(DataFrames):
    
    dataFrame = dataFrame.sort_values(by='GAME_DATE_EST', ascending=True)
    dataFrame['Field Goal Percentage_Diff'] = dataFrame.apply(lambda row: round(row['FG_PCT_home'] - row['FG_PCT_away'], 2), axis=1)
    dataFrame['Free Throw Percentage_Diff'] = dataFrame.apply(lambda row: round(row['FT_PCT_home'] - row['FT_PCT_away'], 2), axis=1)
    dataFrame['Three Point Percentage_Diff'] = dataFrame.apply(lambda row: round(row['FG3_PCT_home'] - row['FG3_PCT_away'], 2), axis=1)
    dataFrame['Assists_Diff'] = dataFrame.apply(lambda row: round(row['AST_home'] - row['AST_away'], 2), axis=1)
    dataFrame['Rebounds_Diff'] = dataFrame.apply(lambda row: round(row['REB_home'] - row['REB_away'], 2), axis=1)
    dataFrame['Rebounds_Diff'] = dataFrame.apply(lambda row: round(row['REB_home'] - row['REB_away'], 2), axis=1)

    DataFrames[i] = dataFrame

    #dataFrame['match_awayteam_position_difference'] = dataFrame.apply(lambda ro,w: row['away_current_pos'] - row['home_current_pos'], axis = 1)
    
    ## Computing the features.
    #computeTGD(dataFrame)
    computeKPP(dataFrame, 4)
    computeStreak(dataFrame, 4)
    #computeForm(dataFrame, 0.33)

    print(i)

## Concatening all the dataframes together.
DataFrame = pd.concat(DataFrames)

## Saving the newly engineered dataset.
DataFrame.to_csv('Article_1_Dataset_3/Data/prepoc_dataset.csv', sep = ',', index = False)