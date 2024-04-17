## Importing necessary libraries and modules.
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

def trainTestSplit(Set):

	DataFrame = pd.read_csv('..\Data\prepoc_dataset.csv')

	## Creating a list of unwanted features
	unwanted = ["GAME_DATE_EST","GAME_ID", "HOME_TEAM_ID", "VISITOR_TEAM_ID", "TEAM_ID_home","TEAM_ID_away","GAME_STATUS_TEXT"]

	## Dropping the above coloumns .
	DataFrame.drop(unwanted, axis = 1, inplace = True)

	## List of features who's initial values are Nan.
	nanFeatures = [ 'Field Goal Percentage_Diff',
	'Free Throw Percentage_Diff',
	'Three Point Percentage_Diff',
	'Assists_Diff',
	'Rebounds_Diff',
	'k_past_points_home',
	'k_past_assists_home',
	'k_past_rebounds_home',
	'k_past_points_away',
	'k_past_assists_away',
	'k_past_rebounds_away',
	'k_past_points_diff',
	'k_past_assists_diff',
	'k_past_rebounds_diff',
	'Home_St',
	'Away_St',
	'Home_StWeighted',
	'Away_StWeighted',
	'Streak',
	'WeightedStreak']

	## Getting a list of the unique seasons.
	seasonNames = list(DataFrame.SEASON.unique())
	dataFramesList = []

	for season in seasonNames:
		
		## Creating a Temporary DataFrame season-wise.
		tempDF = DataFrame[ (DataFrame['SEASON'] == (season) )]
		tempDF = tempDF.dropna(subset = nanFeatures)
		dataFramesList.append(tempDF)

	DataFrame = pd.concat(dataFramesList) 

	## Splitting the data into Training and Testing splits.
	
	## For our "Target Variable" , we need the match outcomes which is the field "FTR" (Full Time Result) .
	## So , we will create a slice of this coloumn as well as "Season" (for indexing purposes) .
	Y = DataFrame[['HOME_TEAM_WINS','SEASON']]

	## Now, we will choose the first 11 seasons as our Training Set and the final 2 as Testing Set.
	YTrain = Y[(Y['SEASON'] == '2003') | (Y['SEASON'] == '2004') | (Y['SEASON'] == '2005') | (Y['SEASON'] == '2006') | 
			(Y['SEASON'] == '2007') | (Y['SEASON'] == '2008') | (Y['SEASON'] == '2009') | (Y['SEASON'] == '2010') |
			(Y['SEASON'] == '2011') | (Y['SEASON'] == '2012') | (Y['SEASON'] == '2013') | (Y['SEASON'] == '2014') | 
			(Y['SEASON'] == '2015') | (Y['SEASON'] == '2016') | (Y['SEASON'] == '2017') | (Y['SEASON'] == '2018')]

	YTest = Y[(Y['SEASON'] == '2019') | (Y['SEASON'] == '2020') | (Y['SEASON'] == '2021') | (Y['SEASON'] == '2022')]

	## Now , we dont need the "Season" coloumn so drop it .
	YTrain.drop(['SEASON'], axis = 1, inplace = True)
	YTest.drop(['SEASON'], axis = 1, inplace = True)

	## Now, for creating the feature set, we first need to remove the target variable from the DataFrame .
## Now, for creating the feature set, we first need to remove the target variable from the DataFrame.
	X = DataFrame
	X.drop(['HOME_TEAM_WINS'], axis=1, inplace=True)

	## Now, we will choose the first 16 seasons as our Training Set and the final 4 as Testing Set.
	XTrain = X[(X['SEASON'] == '2003') | (X['SEASON'] == '2004') | (X['SEASON'] == '2005') | (X['SEASON'] == '2006') | 
			(X['SEASON'] == '2007') | (X['SEASON'] == '2008') | (X['SEASON'] == '2009') | (X['SEASON'] == '2010') |
			(X['SEASON'] == '2011') | (X['SEASON'] == '2012') | (X['SEASON'] == '2013') | (X['SEASON'] == '2014') | 
			(X['SEASON'] == '2015') | (X['SEASON'] == '2016') | (X['SEASON'] == '2017') | (X['SEASON'] == '2018')]

	XTest = X[(X['SEASON'] == '2019') | (X['SEASON'] == '2020') | (X['SEASON'] == '2021') | (X['SEASON'] == '2022')]

	## Now, we don't need the "Season" column so drop it.
	XTrain.drop(['SEASON'], axis=1, inplace=True)
	XTest.drop(['SEASON'], axis=1, inplace=True)
	
	## Splitting the feature set into the appropriate set.
	if (Set == 'A'):

		## The set of features to be added in Set A i.e. the non-differential features.
		nonDifferentialFeatures = [
			'PTS_home',
			'FG_PCT_home',
			'FT_PCT_home',
			'FG3_PCT_home',
			'AST_home',
			'REB_home',
			'PTS_away',
			'FG_PCT_away',
			'FT_PCT_away',
			'FG3_PCT_away',
			'AST_away',
			'REB_away',
			'k_past_points_home',
			'k_past_assists_home',
			'k_past_rebounds_home',
			'k_past_points_away',
			'k_past_assists_away',
			'k_past_rebounds_away',
			'Home_St',
			'Away_St',
			'Home_StWeighted',
			'Away_StWeighted'
		]

		## Choosing the above feature set.
		XTrainA = XTrain[nonDifferentialFeatures]
		XTestA = XTest[nonDifferentialFeatures]

		return XTrainA, XTestA, YTrain, YTest

	if (Set == 'B'):

		## The set of features to be added in Set B i.e. the differential features.
		differentialFeatures = [
			'Field Goal Percentage_Diff',
			'Free Throw Percentage_Diff',
			'Three Point Percentage_Diff',
			'Assists_Diff',
			'Rebounds_Diff',
			'k_past_points_diff',
			'k_past_assists_diff',
			'k_past_rebounds_diff',
			'Streak',
			'WeightedStreak']



		## Choosing the above feature set.
		XTrainB = XTrain[differentialFeatures]
		XTestB = XTest[differentialFeatures]
		
		return XTrainB, XTestB, YTrain, YTest