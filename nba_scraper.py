# nba_season_scraper.py

import csv
import time
from datetime import datetime, timedelta
import sys

# Ensure Python can find the basketball_reference_web_scraper module
sys.path.insert(0, '/Users/ayugpoudel/Documents/Nba Scraper/basketball_reference_web_scraper')

from basketball_reference_web_scraper import client


# Define season start and end dates
season_start_date = datetime(2023, 10, 24)
season_end_date = datetime(2024, 4, 14)



# CSV file to store data
output_file = "nba_season_data.csv"

# Prepare CSV with headers
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    headers = [
        'date', 'slug', 'name', 'team', 'location', 'opponent', 'outcome',
        'seconds_played', 'made_field_goals', 'attempted_field_goals',
        'made_three_point_field_goals', 'attempted_three_point_field_goals',
        'made_free_throws', 'attempted_free_throws', 'offensive_rebounds',
        'defensive_rebounds', 'assists', 'steals', 'blocks', 'turnovers',
        'personal_fouls', 'game_score'
    ]
    writer.writerow(headers)

# Iterate through each day in the season range
current_date = season_start_date
while current_date <= season_end_date:
    try:
        # Get data for the specific day
        data = client.player_box_scores(
            day=current_date.day, month=current_date.month, year=current_date.year
        )
        print(f"Data for {current_date.strftime('%Y-%m-%d')} retrieved successfully.")

        # Append data to CSV
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for player_data in data:
                # Flatten the nested fields (team, location, opponent, outcome) to write into CSV
                row = [
                    current_date.strftime('%Y-%m-%d'),
                    player_data['slug'], player_data['name'], player_data['team'].value,
                    player_data['location'].value, player_data['opponent'].value,
                    player_data['outcome'].value, player_data['seconds_played'],
                    player_data['made_field_goals'], player_data['attempted_field_goals'],
                    player_data['made_three_point_field_goals'], player_data['attempted_three_point_field_goals'],
                    player_data['made_free_throws'], player_data['attempted_free_throws'],
                    player_data['offensive_rebounds'], player_data['defensive_rebounds'],
                    player_data['assists'], player_data['steals'], player_data['blocks'],
                    player_data['turnovers'], player_data['personal_fouls'], player_data['game_score']
                ]
                writer.writerow(row)

    except Exception as e:
        print(f"Error on {current_date.strftime('%Y-%m-%d')}: {e}")

    # Delay to prevent rate limiting
    time.sleep(3)  # Adjust delay as necessary, e.g., 5 seconds

    # Move to the next day
    current_date += timedelta(days=1)

print("Data collection complete.")
