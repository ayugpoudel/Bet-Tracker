import pandas as pd
from scipy.stats import norm

# Load last season's player data
last_season_data = pd.read_csv('/Users/ayugpoudel/Documents/Nba Scraper/nba_season_data.csv')

def calculate_prop_probability(player_name, prop, line, opponent, location='home'):
    # Convert inputs to lower case to handle case insensitivity
    player_name = player_name.lower()
    prop = prop.lower()
    opponent = opponent.lower()
    location = location.lower()
    
    # Filter data for the specific player
    player_data = last_season_data[last_season_data['name'].str.lower() == player_name]

    # Calculate points if the prop is "points"
    if prop == "points":
        player_data['points'] = (
            (player_data['made_field_goals'] - player_data['made_three_point_field_goals']) * 2 +
            player_data['made_three_point_field_goals'] * 3 +
            player_data['made_free_throws']
        )
    if prop == "rebounds":
        player_data['rebounds'] = (
            (player_data['offensive_rebounds'] + player_data['defensive_rebounds'])
        )
    if prop == "pra":
        player_data['pra'] = (
            (((player_data['made_field_goals'] - player_data['made_three_point_field_goals']) * 2 +
            player_data['made_three_point_field_goals'] * 3 +
            player_data['made_free_throws']
            )) + ((player_data['offensive_rebounds'] + player_data['defensive_rebounds'])) + player_data['assists'])
    if prop == "threes":
        player_data['threes'] = (
            (player_data['made_three_point_field_goals'])
        )
    # Calculate season average and standard deviation for the prop
    avg_value = player_data[prop].mean()
    std_dev = player_data[prop].std()

    # Adjust for recent performance (last 5 games of the previous season as an example)
    recent_value = player_data[prop].tail(5).mean()

    # Contextual adjustment using opponent defense, home/away performance
    # Check if opponent defense rating is available
    if 'opponent_def_rating' in player_data.columns:
        opponent_data = player_data[player_data['opponent'].str.lower() == opponent]
        opponent_def_rating = opponent_data['opponent_def_rating'].mean() if not opponent_data.empty else player_data['opponent_def_rating'].mean()
        adjusted_value = avg_value * (1 - (opponent_def_rating / 100))
    else:
        adjusted_value = avg_value  # Use avg_value if opponent defense rating is not available

    # Adjust based on location (home or away)
    if location == 'away' and 'location' in player_data.columns:
        away_games = player_data[player_data['location'] == 'AWAY']
        if not away_games.empty:
            adjusted_value = away_games[prop].mean()

    # Calculate the probability using a normal distribution
    probability = norm.cdf(line, loc=adjusted_value, scale=std_dev)

    # Calculate over and under probability
    over_probability = (1 - probability) * 100
    under_probability = probability * 100

    return {
        "Player": player_name.title(),
        "Prop": prop.title(),
        "Line": line,
        "Opponent": opponent.title(),
        "Location": location.title(),
        "Over %": round(over_probability, 2),
        "Under %": round(under_probability, 2)
    }

# Get user input

repeat = True
while repeat:
    player_name = input("Enter player name: ")
    prop = input("Enter the stat type (e.g., points, rebounds): ")
    line = float(input("Enter the line value: "))
    opponent = input("Enter opponent team: ")
    location = input("Enter location (home/away): ")
    result = calculate_prop_probability(player_name, prop, line, opponent, location) #Run Calculation
    print(result)
    repeat_input = input("Would you like to continue?: ") #Repeat Input
    if repeat_input.lower() == ('no'):
        repeat = False


