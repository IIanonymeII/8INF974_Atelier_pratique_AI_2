import pandas as pd

def loadDataFrameList():

    ## Loading in the datasets for all the league seasons
    df2003_2004 = pd.read_csv('Article_1_Dataset_3/Data/season_2003.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2004_2005 = pd.read_csv('Article_1_Dataset_3/Data/season_2004.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2005_2006 = pd.read_csv('Article_1_Dataset_3/Data/season_2005.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2006_2007 = pd.read_csv('Article_1_Dataset_3/Data/season_2006.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2007_2008 = pd.read_csv('Article_1_Dataset_3/Data/season_2007.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2008_2009 = pd.read_csv('Article_1_Dataset_3/Data/season_2008.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2009_2010 = pd.read_csv('Article_1_Dataset_3/Data/season_2009.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2010_2011 = pd.read_csv('Article_1_Dataset_3/Data/season_2010.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2011_2012 = pd.read_csv('Article_1_Dataset_3/Data/season_2011.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2012_2013 = pd.read_csv('Article_1_Dataset_3/Data/season_2012.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2013_2014 = pd.read_csv('Article_1_Dataset_3/Data/season_2013.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2014_2015 = pd.read_csv('Article_1_Dataset_3/Data/season_2014.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2015_2016 = pd.read_csv('Article_1_Dataset_3/Data/season_2015.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2016_2017 = pd.read_csv('Article_1_Dataset_3/Data/season_2016.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2017_2018 = pd.read_csv('Article_1_Dataset_3/Data/season_2017.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2018_2019 = pd.read_csv('Article_1_Dataset_3/Data/season_2018.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2019_2020 = pd.read_csv('Article_1_Dataset_3/Data/season_2019.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2020_2021 = pd.read_csv('Article_1_Dataset_3/Data/season_2020.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2021_2022 = pd.read_csv('Article_1_Dataset_3/Data/season_2021.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)
    df2022_2023 = pd.read_csv('Article_1_Dataset_3/Data/season_2022.csv' , sep=",", parse_dates=['GAME_DATE_EST'], dayfirst=True)

    ## Defining a list of dataframes for them to be concatenated together .
    DataFrames=[df2003_2004, df2004_2005, df2005_2006, df2006_2007, df2007_2008, df2008_2009, df2009_2010,
                df2010_2011,df2011_2012,df2012_2013,df2013_2014,df2014_2015,df2015_2016,df2016_2017,df2017_2018, df2018_2019,
                df2019_2020, df2020_2021, df2021_2022, df2022_2023]

    ## Defining a list which contains the season names to be added as a coloumn to the dataframe season wise
    SeasonNames = ["2003-2004","2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009","2009-2010",
                   "2010-2011","2011-2012","2012-2013","2013-2014","2014-2015","2015-2016","2016-2017","2017-2018", "2018-2019",
                   "2019-2020","2020-2021","2021-2022","2022-2023"]

    ## Looping over the above two lists to add a "Season" coloumn seasonwise to each dataframe .
    for i in range(0,len(DataFrames)):
        DataFrames[i]["Season"] = SeasonNames[i]
        i = i + 1

    return DataFrames