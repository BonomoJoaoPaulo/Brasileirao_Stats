import os
import pandas as pd
import json

DATA_DIR = os.path.abspath(r"../data")
CSV_PREFIX = 'brasileirao_table_'

clubs = []
clubs_complete = []

for year in range(2003, 2023):
    df = pd.read_csv(f"{DATA_DIR}/{CSV_PREFIX}{year}.csv")
    for club in df['CLUB'][1:]:
        if club not in clubs:
            clubs.append(club)

clubs.sort()

for club in clubs:
    club_dict = {}
    club_participations = []
    club_points = []
    club_positions = []
    club_matches = []
    club_wins = []
    club_draws = []
    club_losts = []
    club_goals = []
    club_goals_against = []
    club_goals_difference = []
    club_performances = []
    club_participations_descriptions = []

    for year in range(2003, 2023):
        df = pd.read_csv(f"{DATA_DIR}/{CSV_PREFIX}{year}.csv")
        if club in df['CLUB'].values:
            club_line = df.loc[df['CLUB'] == club]
            club_participations.append(year)
            club_positions.append(int(club_line.values[0][0]))
            club_points.append(int(club_line.values[0][2]))
            club_matches.append(int(club_line.values[0][3]))
            club_wins.append(int(club_line.values[0][4]))
            club_draws.append(int(club_line.values[0][5]))
            club_losts.append(int(club_line.values[0][6]))
            club_goals.append(int(club_line.values[0][7]))
            club_goals_against.append(int(club_line.values[0][8]))
            club_goals_difference.append(int(club_line.values[0][7]) - int(club_line.values[0][8]))
            club_performances.append(int(club_line.values[0][10]))
            year_index = club_participations.index(year)
            club_participation_dict = {'POSITION': f'{club_positions[year_index]}\u00e9',
                                        'POINTS': club_points[year_index],
                                        'MATCHES': club_matches[year_index],
                                        'WINS': club_wins[year_index],
                                        'DRAWS': club_draws[year_index],
                                        'LOSTS': club_losts[year_index],
                                        'GOALS': club_goals[year_index],
                                        'GOALS AGAINST': club_goals_against[year_index],
                                        'GOALS DIFFERENCE': club_goals_difference[year_index],
                                        'PERFORMANCE (%)': f'{club_performances[year_index]}%'}
            club_participations_descriptions.append(club_participation_dict)


    club_dict['NAME'] = club
    club_dict['YEARS PARTICIPATED'] = club_participations
    club_dict['TOTAL PARTICIPATIONS'] = len(club_participations)
    club_dict['TOTAL POINTS'] = sum(club_points)
    club_dict['TOTAL GOALS'] = sum(club_goals)
    club_dict['TOTAL WINS'] = sum(club_wins)
    club_dict['TOTAL DRAWS'] = sum(club_draws)
    club_dict['TOTAL LOSTS'] = sum(club_losts)
    club_dict['TOTAL GOALS AGAINST'] = sum(club_goals_against)
    club_dict['TOTAL GOALS DIFFERENCE'] = sum(club_goals_difference)
    club_dict['AVERAGE PERFORMANCE'] = f'{int(sum(club_performances)/len(club_participations))}%'
    club_dict['PARTICAPTION DESCRIPTION'] = dict(zip(club_participations, club_participations_descriptions))
    clubs_complete.append(club_dict)


with open(f'{DATA_DIR}/clubs_info.json', 'w') as js:
    #for club in clubs_complete:
    #    json.dump(club, js, indent=4)
    json.dump(clubs_complete, js, indent=4)
