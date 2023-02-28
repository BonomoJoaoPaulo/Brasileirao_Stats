from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

PATH_DIR = os.path.dirname(__file__)


for year in range(2003, 2023):
    website = f'https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{year}_-_S%C3%A9rie_A'
    response = requests.get(website)
    content = response.text

    soup = BeautifulSoup(content, 'lxml')

    tables = soup.find_all('table', class_="wikitable")
    count_tables = 0

    for table in tables:
        count_tables += 1 

        case_0 = ((year in range(2003, 2013) and year != 2005) and count_tables == 2)
        case_1 = (year == 2005 and count_tables == 5)
        case_2 = (year in range(2013, 2020) and count_tables == 3)
        case_3 = ((year == 2020 or year == 2021) and count_tables == 4)
        case_4 = (year == 2022 and count_tables == 3)

        teams = []
        team_position = 0
        count_tr = 0
        
        if case_0 or case_1 or case_2 or case_3:
            for team_info in table.find_all('tr'):
                team = {}
                count_td = 0
                if count_tr != 0:
                    for stats_info in team_info.find_all('td'):
                        match count_td:
                            case 0:
                                team['POSITION'] = stats_info.get_text()
                            case 1:
                                td_as = stats_info.find_all('a')
                                count_a = 0
                                for a in td_as:
                                    count_a += 1
                                    if count_a == 2: 
                                        team['CLUB'] = a.get_text()
                            case 2:
                                if stats_info.find('b'):
                                    team['POINTS'] = stats_info.find('b').get_text()
                                else:    
                                    team['POINTS'] = stats_info.get_text()
                            case 3:
                                team['PLAYED'] = stats_info.get_text()
                            case 4:
                                team['WINS'] = stats_info.get_text()
                            case 5:
                                team['DRAWN'] = stats_info.get_text()
                            case 6:
                                team['LOST'] = stats_info.get_text()
                            case 7:
                                team['GOALS FOR'] = stats_info.get_text()
                            case 8:
                                team['GOALS AGAINST'] = stats_info.get_text()
                            case 9:
                                team['GOAL DIFFERENCE'] = stats_info.get_text()
                            case 10:
                                team['%'] = stats_info.get_text()

                        count_td += 1
                count_tr += 1
                teams.append(team)

            clubs_df = pd.DataFrame(teams)
            clubs_df.to_csv(f'{PATH_DIR}/data/brasileirao_table_{year}.csv', index=False)
            
        elif case_4:
            for team_info in table.find_all('tr'):
                team = {}
                count_td = 0
                if count_tr != 0:
                    team['POSITION'] = team_info.find('th').get_text()
                    for stats_info in team_info.find_all('td'):
                        match count_td:
                            case 0:
                                td_as = stats_info.find_all('a')
                                count_a = 0
                                for a in td_as:
                                    count_a += 1
                                    if count_a == 2: 
                                        team['CLUB'] = a.get_text()
                            case 1: 
                                team['POINTS'] = stats_info.get_text()
                            case 2:
                                team['PLAYED'] = stats_info.get_text()
                            case 3:
                                team['WINS'] = stats_info.get_text()
                            case 4:
                                team['DRAWN'] = stats_info.get_text()
                            case 5:
                                team['LOST'] = stats_info.get_text()
                            case 6:
                                team['GOALS FOR'] = stats_info.get_text()
                            case 7:
                                team['GOALS AGAINST'] = stats_info.get_text()
                            case 8:
                                team['GOAL DIFFERENCE'] = stats_info.get_text()

                        count_td += 1

                    points = int(team['POINTS'][:2])
                    played = int(team['PLAYED'][:2])
                    team['%'] = int(points/(played*3)*100)

                count_tr += 1
                teams.append(team)

            clubs_df = pd.DataFrame(teams)
            clubs_df.to_csv(f'{PATH_DIR}/data/brasileirao_table_{year}.csv', index=False)


print('FINISH WEB SCRAPING.')
