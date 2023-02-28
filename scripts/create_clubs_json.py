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

    for year in range(2003, 2023):
        df = pd.read_csv(f"{DATA_DIR}/{CSV_PREFIX}{year}.csv")
        if club in df['CLUB'].values:
            club_participations.append(year)

    club_dict['NAME'] = club
    club_dict['PARTICIPATIONS'] = len(club_participations)
    club_dict['YEARS PARTICIPATED'] = club_participations
    clubs_complete.append(club_dict)


with open(f'{DATA_DIR}/clubs_info.json', 'w') as js:
    #for club in clubs_complete:
    #    json.dump(club, js, indent=4)
    json.dump(clubs_complete, js, indent=4)
