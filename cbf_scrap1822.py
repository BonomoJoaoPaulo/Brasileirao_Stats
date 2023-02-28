from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

PATH_DIR = os.path.dirname(__file__)

# ON CBF WEBSITE, THE FRONT-END IS DIFERENT TO TABLES BEFORE AND AFTER 2017;
for y in range(2018, 2023):
    year = y
    website = f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{year}'
    response = requests.get(website)
    content = response.text

    soup = BeautifulSoup(content, 'lxml')

    table = soup.find('table', class_="table m-b-20 tabela-expandir")

    teams = []
    team_position = 0

    for team_info in table.find_all('tr', class_='expand-trigger'):
        team = {}
        team_position += 1
        team['POSITION'] = str(team_position)
        team['CLUB'] = team_info.find('span', class_='hidden-xs').get_text()[:-5]
        team['FU'] = team_info.find('span', class_='hidden-xs').get_text()[-2:]
        team['POINTS'] = team_info.find('th').get_text()
        count_td = 0
        for stats_info in team_info.find_all('td'):
            match count_td:
                case 1:
                    team['PLAYED'] = stats_info.get_text()
                case 2:
                    team['WINS'] = stats_info.get_text()
                case 3:
                    team['DRAWN'] = stats_info.get_text()
                case 4:
                    team['LOST'] = stats_info.get_text()
                case 5:
                    team['GOALS FOR'] = stats_info.get_text()
                case 6:
                    team['GOALS AGAINST'] = stats_info.get_text()
                case 7:
                    team['GOAL DIFFERENCE'] = stats_info.get_text()
                case 8:
                    team['YELLOW CARD'] = stats_info.get_text()
                case 9:
                    team['RED CARD'] = stats_info.get_text()
                case 10:
                    team['%'] = stats_info.get_text()

            count_td += 1

        teams.append(team)

    clubs_df = pd.DataFrame(teams)

    clubs_df.to_csv(f'{PATH_DIR}/data/brasileirao_table_{year}.csv', index=False)
