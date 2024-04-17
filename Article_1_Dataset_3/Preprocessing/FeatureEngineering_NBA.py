#Importing necessary libraries and modules.
import warnings
import numpy as np
import pandas as pd 


warnings.filterwarnings('ignore')

## Loading the list of DataFrames from DataPreprocessing.
DataFrame = pd.read_csv('Article_1_Dataset_3\Data\games.csv')

Dataframe_dif = pd.DataFrame()

print(DataFrame.head(5))

a = 5

'''-----------------------------------     Adding Total Position Difference as a Feature  --------------------------------------------'''
## Creating a function that computes the columns "home_team_total_position_difference" and "away_team_total_position_difference"  .
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

        ## Appending the appropriate "Goal Difference" values to the DataFrame .
        for j in range(0, matches_played):

            if (gameIndices[j] in indexHome):
                DataFrame['home_team_total_position_difference'][gameIndices[j]] = GDList[j]
            elif (gameIndices[j] in indexAway):
                DataFrame['away_team_total_position_difference'][gameIndices[j]] = GDList[j]

    ## Filling in the columns for "GD".
    DataFrame['home_away_total_position_differential'] = DataFrame.apply(lambda row: row['home_team_total_position_difference'] - row['away_team_total_position_difference'], axis = 1)


''''-----------------------------------     Adding KPP as a Feature  --------------------------------------------'''

## Creating a function which computes the KPP (K-Past Performance) feature for Goals, Corners and Shots on Target.

def computeKPP(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).home_team.unique())

    number_teams = len(Teams)
    
    ## Initialising the values contained in the coloumns "HGKPP , HCKPP , HSTKPP" and "AGKPP , ACKPP , ASTKPP". (KPP Features).
    DataFrame['k_past_position_home'] = np.nan
    DataFrame['k_past_rest_time_home'] = np.nan
    
    DataFrame['k_past_position_away'] = np.nan
    DataFrame['k_past_rest_time_away'] = np.nan

    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, number_teams):

        matches_played = ((DataFrame['home_team'] == Teams[z]) | (DataFrame['away_team'] == Teams[z])).sum()

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['home_team'] == str(Teams[z])) | ( DataFrame['away_team'] == str(Teams[z]))]

        ## Creating a list which contains Goals, Corners and Number of Shots on Target for the team under observation match-wise.
        Positions = []
        RestTimes = []

        for index, row in tempDF.iterrows():
    
            if (Teams[z] == row['home_team']):
                Positions.append(float(row['home_current_pos']))
                RestTimes.append(float(row['home_team_rest_time']))

            elif (Teams[z] == row['away_team']):
                Positions.append(float(row['away_current_pos']))
                RestTimes.append(float(row['away_team_rest_time']))

        ## Creating lists to hold values for the corresponding KPP Features.
        # Since these features will be non existent for the first k matches of each team, fill Nan for the first k values.
        positionsKPP = [np.nan] * k
        resttimesKPP = [np.nan] * k
        
        ## Adding appropriate values to the list.
        ## The number of computations performed will be (n + 1 - k) where :
        ## n = number of matches in the season for each team (38).
        ## k = sliding window hyper-parameter.
        for i in range(0, (matches_played + 1 - k)):

            ## Obtaining the slice of records to be observed.
            ## Sum the slice of records and normalize it by k.
            positionSliceSum = sum(Positions[i : (i + k)])/k
            resttimesSliceSum = sum(RestTimes[i : (i + k)])/k

            ## Appending to the list of the corresponding KPP features.
            positionsKPP.append(positionSliceSum)
            resttimesKPP.append(resttimesSliceSum)
            
        ## Creating a list for the index values of the games contained in the tempDF.
        gameIndices = tempDF.index.tolist()

        ## Creating two lists which contains the index number of those games wherein the team under observation was Home or Away.
        indexHome = []
        indexAway = []

        ## Segregate home and away match indices.
        for index, row in tempDF.iterrows():
            
            if (Teams[z] == row['home_team']):
                 indexHome.append(index)

            elif (Teams[z] == row['away_team']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the DataFrame.
        for j in range(0, matches_played):

            if (gameIndices[j] in indexHome):
                DataFrame['k_past_position_home'][gameIndices[j]] = positionsKPP[j]
                DataFrame['k_past_rest_time_home'][gameIndices[j]] = resttimesKPP[j]

            elif (gameIndices[j] in indexAway):
                DataFrame['k_past_position_away'][gameIndices[j]] = positionsKPP[j]
                DataFrame['k_past_rest_time_away'][gameIndices[j]] = resttimesKPP[j]
        
    
    ## Filling in the coloumns for "GKPP, CKPP, STKPP".
    DataFrame['k_past_positions_differential'] = DataFrame.apply(lambda row: row['k_past_position_home'] - row['k_past_position_away'], axis = 1)
    DataFrame['k_past_resttimes_differential'] = DataFrame.apply(lambda row: row['k_past_rest_time_home'] - row['k_past_rest_time_away'], axis = 1)


''''-----------------------------------     Adding Streak and Weighted Streak as a Feature  --------------------------------------------'''

## Creating a function which computes the Streak and Weighted Streak.

def computeStreak(DataFrame, slidingWindowParameter):
    
    ## Set slidingWindowParameter to k.
    k = slidingWindowParameter

    ## Creating a list of all the teams that played in that season.
    Teams = list((DataFrame).home_team.unique())

    number_teams = len(Teams)
    
    ## Initialsing the values in the coloumns "HSt, ASt , HStWeigted , AStWeigted".
    DataFrame['Home_St'] = np.nan
    DataFrame['Away_St'] = np.nan
    DataFrame['Home_StWeighted'] = np.nan
    DataFrame['Away_StWeighted'] = np.nan
    
    ## Creating a Temporary DataFrame which consists of the records of the matches teamwise.
    for z in range(0, number_teams):

        matches_played = ((DataFrame['home_team'] == Teams[z]) | (DataFrame['away_team'] == Teams[z])).sum()

        ## Creating a Temporary DataFrame where the team was either "Home" or "Away" .
        tempDF = DataFrame[(DataFrame['home_team'] == str(Teams[z])) | ( DataFrame['away_team'] == str(Teams[z]))]
    
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
            
            if (Teams[z] == row['home_team']):
                if (row['result'] == 1) :
                    matchPoints.append(3.0)
                elif (row['result'] == 0) :
                    matchPoints.append(0)

            elif (Teams[z] == row['away_team']):
                if (row['result'] == 1) :
                    matchPoints.append(0.0)
                elif (row['result'] == 0) :
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

            if (Teams[z] == row['home_team']):
                 indexHome.append(index)

            elif (Teams[z] == row['away_team']):
                indexAway.append(index)

        ## Appending the appropriate "KPP" values to the DataFrame.
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
    Teams = list((DataFrame).home_team.unique())

    for teamName in Teams :

        ## Initialising values.
        gFormDict[teamName] = 1.0
        matchCounterDict[teamName] = 0

        ## For each team playing in the season, create a temporary DataFrame to record the match numbers of each team.
        ## Create a temporary DataFrame for the team under consideration.
        tempDF = DataFrame[(DataFrame['home_team'] == str(teamName)) | ( DataFrame['AwayTeam'] == str(teamName))]

        ## Assigning match indices list to the relevant team.
        teamMatchLookup[teamName] =  tempDF.index.tolist()

    ## Iterating over each match in the season.
    for index, row in DataFrame.iterrows():
        
        ## Exit condition. Since the last update in the form values will be in the 2nd last match for each team, we have to run the loop till each team's 2nd last match.
        ## This condition happens at the 370th in each season.
        if (index == 370):
        
            break

        ## Update match counter for the playing teams.
        matchCounterDict[row['home_team']] += 1
        matchCounterDict[row['AwayTeam']] += 1

        ## Case where home team wins. Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team.        
        if (row['FTR'] == 'H'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['home_team']]
            prevAwayForm = gFormDict[row['AwayTeam']]

            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['home_team']][matchCounterDict[row['home_team']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]
    
            ## Since the home team wins here, a positive update is given to the home team and a negative update is given to the away team. 
            homeUpdate = gFormDict[row['home_team']] + k * gFormDict[row['AwayTeam']]
            awayUpdate = gFormDict[row['AwayTeam']] - k * gFormDict[row['AwayTeam']]

            ## Selecting next match record for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['home_team'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['home_team']] = homeUpdate

            ## Selecting next match record for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['home_team'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate


        ## Case where away team wins. Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
        if (row['FTR'] == 'A'):

            ## Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['home_team']]
            prevAwayForm = gFormDict[row['AwayTeam']]
        
            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['home_team']][matchCounterDict[row['home_team']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]

            ## Since the away team wins here, a positive update is given to the away team and a negative update is given to the home team.        
            homeUpdate = gFormDict[row['home_team']] - k * gFormDict[row['home_team']]
            awayUpdate = gFormDict[row['AwayTeam']] + k * gFormDict[row['home_team']]

            ## Selecting next match for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['home_team'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['home_team']] = homeUpdate

            ## Selecting next match for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['home_team'][nextMatchA] == row['AwayTeam']):            
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate

        ## Case where a draw occurs.
        if (row['FTR'] == 'D'):

            # Form values of the teams before coming into the match.
            prevHomeForm = gFormDict[row['home_team']]
            prevAwayForm = gFormDict[row['AwayTeam']]
    
            ## Next match index of the Home and Away Team.
            nextMatchH = teamMatchLookup[row['home_team']][matchCounterDict[row['home_team']]]
            nextMatchA = teamMatchLookup[row['AwayTeam']][matchCounterDict[row['AwayTeam']]]

            ## Form Updates.
            homeUpdate = gFormDict[row['home_team']] - k * ((gFormDict[row['home_team']]) - (gFormDict[row['AwayTeam']]))
            awayUpdate = gFormDict[row['AwayTeam']] - k * ((gFormDict[row['AwayTeam']]) - (gFormDict[row['home_team']]))

            ## Selecting next match for the current Home Team.
            matchInfoH = DataFrame.iloc[[nextMatchH]]

            ## Check whether current Home Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoH['home_team'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'HForm'] = homeUpdate

            elif (matchInfoH['AwayTeam'][nextMatchH] == row['home_team']):
                DataFrame.loc[nextMatchH, 'AForm'] = homeUpdate

            ## Update value in the dictionary.
            gFormDict[row['home_team']] = homeUpdate

            ## Selecting next match for the current Away Team.
            matchInfoA = DataFrame.iloc[[nextMatchA]]

            ## Check whether current Away Team is Home or Away in their next match and update Form accordingly.
            if (matchInfoA['home_team'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'HForm'] = awayUpdate

            elif (matchInfoA['AwayTeam'][nextMatchA] == row['AwayTeam']):
                DataFrame.loc[nextMatchA, 'AForm'] = awayUpdate

            ## Update value in the dictionary.
            gFormDict[row['AwayTeam']] = awayUpdate
    
    # Filling in the coloumns for "Form".
    DataFrame['Form'] = DataFrame.apply(lambda row: row['HForm'] - row['AForm'], axis = 1)


## Computing features for all the data.
    
Dataframe_dif['Points_Diff'] = DataFrame.apply(lambda row: row['PTS_home'] - row['PTS_away'], axis = 1)
Dataframe_dif['Field Goal Percentage_Diff'] = DataFrame.apply(lambda row: row['FG_PCT_home'] - row['FG_PCT_away'], axis = 1)
Dataframe_dif['Free Throw Percentage_Diff'] = DataFrame.apply(lambda row: row['FT_PCT_home'] - row['FT_PCT_away'], axis = 1)
Dataframe_dif['Three Point Percentage_Diff'] = DataFrame.apply(lambda row: row['FG3_PCT_home'] - row['FG3_PCT_away'], axis = 1)
Dataframe_dif['Assists_Diff'] = DataFrame.apply(lambda row: row['AST_home'] - row['AST_away'], axis = 1)
Dataframe_dif['Rebounds_Diff'] = DataFrame.apply(lambda row: row['REB_home'] - row['REB_away'], axis = 1)

#DataFrame['match_awayteam_position_difference'] = DataFrame.apply(lambda row: row['away_current_pos'] - row['home_current_pos'], axis = 1)
    
## Computing the features.
#computeTGD(DataFrame)
#computeKPP(DataFrame, 4)
#computeStreak(DataFrame, 4)
#computeForm(DataFrame, 0.33)

## Saving the newly engineered dataset.
Dataframe_dif.to_csv('Article_1_Dataset_3\Data\prepoc_dataset.csv', sep = ',', index = False)