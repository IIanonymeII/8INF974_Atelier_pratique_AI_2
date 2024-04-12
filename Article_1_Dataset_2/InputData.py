import pandas as pd

def loadDataFrameList():

    ## Loading in the datasets for all the league seasons
    df2010_2011 = pd.read_csv('Article_1_Dataset_2/Dataset/2010-11.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2011_2012 = pd.read_csv('Article_1_Dataset_2/Dataset/2011-12.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2012_2013 = pd.read_csv('Article_1_Dataset_2/Dataset/2012-13.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2013_2014 = pd.read_csv('Article_1_Dataset_2/Dataset/2013-14.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2014_2015 = pd.read_csv('Article_1_Dataset_2/Dataset/2014-15.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2015_2016 = pd.read_csv('Article_1_Dataset_2/Dataset/2015-16.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2016_2017 = pd.read_csv('Article_1_Dataset_2/Dataset/2016-17.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2017_2018 = pd.read_csv('Article_1_Dataset_2/Dataset/2017-18.csv' , sep=",", parse_dates=['Date'], dayfirst=True)
    df2018_2019 = pd.read_csv('Article_1_Dataset_2/Dataset/2018-19.csv' , sep=",", parse_dates=['Date'], dayfirst=True)

    ## Defining a list of dataframes for them to be concatenated together .
    DataFrames=[df2010_2011,df2011_2012,df2012_2013,df2013_2014,df2014_2015,df2015_2016,df2016_2017,df2017_2018, df2018_2019]

    ## Defining a list which contains the season names to be added as a coloumn to the dataframe season wise
    SeasonNames = ["2010-2011","2011-2012","2012-2013","2013-2014","2014-2015","2015-2016","2016-2017","2017-2018", "2018-2019"]

    ## Looping over the above two lists to add a "Season" coloumn seasonwise to each dataframe .
    for i in range(0,len(DataFrames)):
        DataFrames[i]["Season"] = SeasonNames[i]
        i = i + 1

    return DataFrames