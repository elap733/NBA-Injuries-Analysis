# -*- coding: utf-8 -*-
"""
This script is used to creates two dictionaries of NBA team abbreviation and
nicknames respectively, and saves these dictionaries as pickles.

@author: evanl
"""
import pickle

team_nickname_dict = {
    'Hawks': 'Atlanta Hawks',
    'Celtics': 'Boston Celtics',
    'Bobcats': 'Charlotte Bobcats',
    'Bulls': 'Chicago Bulls',
    'Cavaliers': 'Cleveland Cavaliers',
    'Mavericks': 'Dallas Mavericks',
    'Nuggets': 'Denver Nuggets',
    'Pistons': 'Detroit Pistons',
    'Warriors': 'Golden State Warriors',
    'Rockets': 'Houston Rockets',
    'Pacers': 'Indiana Pacers',
    'Clippers': 'Los Angeles Clippers',
    'Lakers': 'Los Angeles Lakers',
    'Grizzlies': 'Memphis Grizzlies',
    'Heat': 'Miami Heat',
    'Bucks': 'Milwaukee Bucks',
    'Timberwolves': 'Minnesota Timberwolves',
    'Pelicans': 'New Orleans Pelicans',
    'Knicks': 'New York Knicks',
    'Thunder': 'Oklahoma City Thunder',
    'Magic': 'Orlando Magic',
    '76ers': 'Philadelphia 76ers',
    'Suns': 'Phoenix Suns',
    'Blazers': 'Portland Trailblazers',
    'Kings': 'Sacramento Kings',
    'Spurs': 'San Antonio Spurs',
    'Raptors': 'Toronto Raptors',
    'Jazz': 'Utah Jazz',
    'Wizards': 'Washington Wizards',
    'New Jersey Nets':'New Jersey Nets',
    'Brooklyn Nets':'Brooklyn Nets',
    'New Orleans Hornets':'New Orleans Hornets',
    'Charlotte Hornets':'Charlotte Hornets',
}

team_abrv_dict = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Bobcats',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trailblazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards',
    'NJN': 'New Jersey Nets',
    'BRK': 'Brooklyn Nets',
    'NOH': 'New Orleans Hornets',
    'CHO': 'Charlotte Hornets',
    'SEA': 'Seattle Supersonics',
    'CHH': 'Charlotte Hornets',
    'WSB': 'Washington Bullets',
    'NOK': 'New Orleans Hornets',
    'VAN': 'Vancouver Grizzlies',
}

print('Saving files...')

pickle.dump(team_nickname_dict, open( 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/teams_nickname_dictionary.p', "wb" ) )
pickle.dump(team_abrv_dict, open( 'C:/Users/evanl/OneDrive/Desktop/DS Projects/NBA Injury Project/Scraped_Data/teams_abrv_dictionary.p', "wb" ) )

print('Finished')