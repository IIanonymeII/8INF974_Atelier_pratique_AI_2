## Importing necessary libraries and modules.
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

def trainTestSplit(Set):

	DataFrame = pd.read_csv('..\Dataset\concatenated.csv', delimiter = ',')

	## Creating a list of unwanted features
	unwanted = ["Date","month", "year", "away_team", "home_team"]

	## Dropping the above coloumns .
	DataFrame.drop(unwanted, axis = 1, inplace = True)

	## List of features who's initial values are Nan.
	nanFeatures = ['k_past_position_home', 'k_past_rest_time_home', 'k_past_position_away', 'k_past_rest_time_away', 'k_past_positions_differential', 
				'k_past_resttimes_differential', 'Home_St', 'Away_St', 'Home_StWeighted', 'Away_StWeighted', 
				'Streak', 'WeightedStreak']

	## Getting a list of the unique seasons.
	seasonNames = list(DataFrame.Season.unique())
	dataFramesList = []
	
	for season in seasonNames:
		
		## Creating a Temporary DataFrame season-wise.
		tempDF = DataFrame[ (DataFrame['Season'] == (season) )]
		tempDF = tempDF.dropna(subset = nanFeatures)
		dataFramesList.append(tempDF)
	

	DataFrame = pd.concat(dataFramesList)

	## Splitting the data into Training and Testing splits.
	
	## For our "Target Variable" , we need the match outcomes which is the field "FTR" (Full Time Result) .
	## So , we will create a slice of this coloumn as well as "Season" (for indexing purposes) .
	Y = DataFrame[['result','Season']]

	## Now , we will choose the first 11 seasons as our Training Set and the final 2 as Testing Set .
	YTrain = Y[ (Y['Season'] == '2010-2011') | (Y['Season'] == '2011-2012') | (Y['Season'] == '2012-2013') | (Y['Season'] == '2013-2014') | 
			(Y['Season'] == '2014-2015') | (Y['Season'] == '2015-2016') | (Y['Season'] == '2016-2017')]         
	YTest = Y[(Y['Season'] == '2017-2018') | (Y['Season'] == '2018-2019')]

	## Now , we dont need the "Season" coloumn so drop it .
	YTrain.drop(['Season'], axis = 1, inplace = True)
	YTest.drop(['Season'], axis = 1, inplace = True)

	## Now, for creating the feature set, we first need to remove the target variable from the DataFrame .
	X = DataFrame
	X.drop(['result'], axis = 1, inplace = True)

	## Now , we will choose the first 11 seasons as our Training Set and the final 2 as Testing Set .
	XTrain = X[ (X['Season'] == '2010-2011') | (X['Season'] == '2011-2012') | (X['Season'] == '2012-2013') | (X['Season'] == '2013-2014') | 
			(X['Season'] == '2014-2015') | (X['Season'] == '2015-2016')| (X['Season'] == '2016-2017')] 
	XTest = X[ (X['Season'] == '2017-2018') | (X['Season'] == '2018-2019')]

	## Now , we dont need the "Season" coloumn so drop it .
	XTrain.drop(['Season'], axis = 1, inplace = True)
	XTest.drop(['Season'], axis = 1, inplace = True)
	
	## Splitting the feature set into the appropriate set.
	if (Set == 'A'):

		nonDifferentialFeatures = ['Unnamed: 0',
		'away_current_pos',
		'away_last_yr_pos',
		'away_prev_game_perf',
		'away_team_av_points',
		'away_team_av_points_conceded',
		'away_team_away_form',
		'away_team_form',
		'away_team_rest_time',
		'away_win_percentage',
		'home_current_pos',
		'home_last_yr_pos',
		'home_prev_game_perf',
		'home_team_av_points',
		'home_team_av_points_conceded',
		'home_team_form',
		'home_team_home_form',
		'home_team_rest_time',
		'home_win_percentage',
		'k_past_position_home',
		'k_past_rest_time_home',
		'k_past_position_away',
		'k_past_rest_time_away',
		'Home_St',
		'Away_St',
		'Home_StWeighted',
		'Away_StWeighted',
		]

		## Choosing the above feature set.
		XTrainA = XTrain[nonDifferentialFeatures]
		XTestA = XTest[nonDifferentialFeatures]

		return XTrainA, XTestA, YTrain, YTest

	if (Set == 'B'):

		differentialFeatures = [
		'h2h_form',

		'match_importance',
		'HomeAway_Position_Differntial',
		'HomeAway_Form_Differntial',
		'HomeAway_Average_Points_Differntial',
		'HomeAway_Average_Points_Conceded_Differntial',
		'HomeAway_Win_Precentage_Differntial',


		'k_past_positions_differential',
		'k_past_resttimes_differential',
		'Streak',
		'WeightedStreak']



		## Choosing the above feature set.
		XTrainB = XTrain[differentialFeatures]
		XTestB = XTest[differentialFeatures]

		return XTrainB, XTestB, YTrain, YTest