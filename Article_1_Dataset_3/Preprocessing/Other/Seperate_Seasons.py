import pandas as pd

# Read the dataset
data = pd.read_csv('Article_1_Dataset_3\Data\games.csv')

# Separate datasets based on season
seasons = data['SEASON'].unique()

for season in seasons:
    season_data = data[data['SEASON'] == season]
    season_data.to_csv(f'season_{season}.csv', index=False)
