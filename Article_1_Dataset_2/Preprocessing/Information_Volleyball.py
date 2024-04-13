import csv

def count_games(csv_file):
    team_games = {}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            away_team = row['away_team']
            home_team = row['home_team']

            if away_team in team_games:
                team_games[away_team] += 1
            else: 
                team_games[away_team] = 1

            if home_team in team_games:
                team_games[home_team] += 1
            else:
                team_games[home_team] = 1

    return team_games

if __name__ == "__main__":
    team_games = count_games("Article_1_Dataset_2/Dataset/2013-14.csv")
    for team, games in team_games.items():
        print(f"{team}: {games} games played")
