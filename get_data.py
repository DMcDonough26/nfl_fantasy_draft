import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import timeit
import numpy as np

def get_rankings():

    site = 'https://www.espn.com/fantasy/football/story/_/page/ffcheatsheet22/fantasy-football-cheat-sheets-updated-2022-player-rankings-ppr-non-ppr-depth-charts-dynasty'
    pdf = 'https://g.espncdn.com/s/ffldraftkit/22/NFLDK2022_CS_NonPPR300.pdf'

    raw_df = pd.read_csv('top_300_2022.csv')
    # raw_df = pd.read_csv('top_300_ppr_2022.csv')
    raw_df = raw_df.drop([1068,1165]).reset_index(drop=True).copy()

    rank = []
    player = []
    position = []
    team = []
    bye = []
    posrank = []

    for i in range(1200):

        if i%4 == 0:
            # rank
            rank.append(int(raw_df.iloc[i].values[0].split('.')[0]))
            position.append(raw_df.iloc[i].values[0].split('.')[1].split('(')[1].split(")")[0][0])
            tempval = raw_df.iloc[i].values[0].split('.')[1].split('(')[1].split(")")[0]
            if tempval[0] in ['Q','R','W','T']:
                if len(tempval) == 5:
                    posrank.append(int(tempval[-3:]))
                if len(tempval) == 4:
                    posrank.append(int(tempval[-2:]))
                if len(tempval) == 3:
                    posrank.append(int(tempval[-1:]))
            if tempval[0] == 'D':
                if len(tempval) == 5:
                    posrank.append(int(tempval[-2:]))
                if len(tempval) == 4:
                    posrank.append(int(tempval[-1:]))
            if tempval[0] == 'K':
                if len(tempval) == 3:
                    posrank.append(int(tempval[-2:]))
                if len(tempval) == 2:
                    posrank.append(int(tempval[-1:]))

        if i%4 == 1:
            # name
            player.append(raw_df.iloc[i].values[0].split(', ')[0])
            team.append(raw_df.iloc[i].values[0].split(', ')[1])
        if i%4 == 2:
            # money
            pass
        if i%4 == 3:
            # bye
            bye.append(int(raw_df.iloc[i].values[0]))

    player_rankings = pd.DataFrame({'rank':rank,'player':player,'position':position,'team':team,'bye':bye,'posrank':posrank}).sort_values(by='rank')

    return player_rankings

def scrape_qb():
    url = 'https://www.fantasypros.com/nfl/projections/qb.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    attempts = []
    completions = []
    yards = []
    touchdowns = []
    interceptions = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []
    for i in range(30):
        name = len(str(soup.findAll('td')[4+11*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+11*i].findAll('a')[0]).split('>')[1][0:name-3])
        attempts.append(float(str(soup.findAll('td')[5+11*i]).split('>')[1].split('<')[0]))
        completions.append(float((str(soup.findAll('td')[6+11*i]).split('>')[1].split('<')[0])))
        yards.append(float(str(soup.findAll('td')[7+11*i]).split('>')[1].split('<')[0].split(',')[0]+str(soup.findAll('td')[7+11*i]).split('>')[1].split('<')[0].split(',')[1]))
        touchdowns.append(float((str(soup.findAll('td')[8+11*i]).split('>')[1].split('<')[0])))
        interceptions.append(float((str(soup.findAll('td')[9+11*i]).split('>')[1].split('<')[0])))
        rush_attempts.append(float((str(soup.findAll('td')[10+11*i]).split('>')[1].split('<')[0])))
        rush_yards.append(float((str(soup.findAll('td')[11+11*i]).split('>')[1].split('<')[0])))
        rush_tds.append(float((str(soup.findAll('td')[12+11*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[13+11*i]).split('>')[1].split('<')[0])))

    qb_projections = pd.DataFrame({'player_stat':player_stat,'attempts':attempts,'completions':completions,'yards':yards,
                             'touchdowns':touchdowns,'interceptions':interceptions,'rush_attempts':rush_attempts,
                             'rush_yards':rush_yards,'rush_tds':rush_tds,'fumbles':fumbles})

    return qb_projections

def scrape_rb():
    url = 'https://www.fantasypros.com/nfl/projections/rb.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    receptions = []
    receive_yards = []
    receive_tds = []
    fumbles = []
    for i in range(100):
        name = len(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1][0:name-3])
        rush_attempts.append(float((str(soup.findAll('td')[5+9*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]) < 6:
            rush_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0])))
        else:
            rush_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]).split(',')[0]+(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]).split(',')[1]))
        rush_tds.append(float((str(soup.findAll('td')[7+9*i]).split('>')[1].split('<')[0])))
        receptions.append(float((str(soup.findAll('td')[8+9*i]).split('>')[1].split('<')[0])))
        receive_yards.append(float((str(soup.findAll('td')[9+9*i]).split('>')[1].split('<')[0])))
        receive_tds.append(float((str(soup.findAll('td')[10+9*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[11+9*i]).split('>')[1].split('<')[0])))

    rb_projections = pd.DataFrame({'player_stat':player_stat,'rush_attempts':rush_attempts,'rush_yards':rush_yards,
                                   'rush_tds':rush_tds,'receptions':receptions,'receive_yards':receive_yards,
                                   'receive_tds':receive_tds,'fumbles':fumbles})

    return rb_projections

def scrape_wr():
    url = 'https://www.fantasypros.com/nfl/projections/wr.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    receptions = []
    receive_yards = []
    receive_tds = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []
    for i in range(100):
        name = len(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1][0:name-3])
        receptions.append(float((str(soup.findAll('td')[5+9*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]) < 6:
            receive_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0])))
        else:
            receive_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0].split(',')[0]+str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0].split(',')[1])))
        receive_tds.append(float((str(soup.findAll('td')[7+9*i]).split('>')[1].split('<')[0])))
        rush_attempts.append(float((str(soup.findAll('td')[8+9*i]).split('>')[1].split('<')[0])))
        rush_yards.append(float((str(soup.findAll('td')[9+9*i]).split('>')[1].split('<')[0])))
        rush_tds.append(float((str(soup.findAll('td')[10+9*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[11+9*i]).split('>')[1].split('<')[0])))

    wr_projections = pd.DataFrame({'player_stat':player_stat,'receptions':receptions,'receive_yards':receive_yards,
                                   'receive_tds':receive_tds,'rush_attempts':rush_attempts,'rush_yards':rush_yards,
                                   'rush_tds':rush_tds,'fumbles':fumbles})

    return wr_projections

def scrape_te():
    url = 'https://www.fantasypros.com/nfl/projections/te.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    receptions = []
    receive_yards = []
    receive_tds = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []
    for i in range(80):
        name = len(str(soup.findAll('td')[3+6*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[3+6*i].findAll('a')[0]).split('>')[1][0:name-3])
        receptions.append(float((str(soup.findAll('td')[4+6*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0]) < 6:
            receive_yards.append(float((str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0])))
        else:
            receive_yards.append(float(str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0].split(',')[0]+str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0].split(',')[1]))
        receive_tds.append(float((str(soup.findAll('td')[6+6*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[7+6*i]).split('>')[1].split('<')[0])))

    te_projections = pd.DataFrame({'player_stat':player_stat,'receptions':receptions,'receive_yards':receive_yards,
                                   'receive_tds':receive_tds,'fumbles':fumbles})

    return te_projections

def scrape_dst():
    url = 'https://www.fantasypros.com/nfl/projections/dst.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    sack = []
    interception = []
    fumble_recovered = []
    touchdowns = []
    safety = []
    points_against = []
    yards_against = []



    for i in range(32):
        name = len(str(soup.findAll('td')[0+10*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[0+10*i].findAll('a')[0]).split('>')[1][0:name-3])
        sack.append(float((str(soup.findAll('td')[1+10*i]).split('>')[1].split('<')[0])))
        interception.append(float((str(soup.findAll('td')[2+10*i]).split('>')[1].split('<')[0])))
        fumble_recovered.append(float((str(soup.findAll('td')[3+10*i]).split('>')[1].split('<')[0])))
        touchdowns.append(float((str(soup.findAll('td')[5+10*i]).split('>')[1].split('<')[0])))
        safety.append(float((str(soup.findAll('td')[6+10*i]).split('>')[1].split('<')[0])))
        points_against.append(float((str(soup.findAll('td')[7+10*i]).split('>')[1].split('<')[0])))
        yards_against.append((str(soup.findAll('td')[8+10*i]).split('>')[1].split('<')[0]))

    dst_projections = pd.DataFrame({'player_stat':player_stat,'sack':sack,'interception':interception,
                                   'fumble_recovered':fumble_recovered,'touchdowns':touchdowns,
                                   'safety':safety,'points_against':points_against,'yards_against':yards_against})

    # this should have originally been written as an apply function
    for i in range(32):
        dst_projections['player_stat'][i] = dst_projections['player_stat'][i].split(' ')[-1] + ' D/ST'

    return dst_projections

def scrape_k():
    url = 'https://www.fantasypros.com/nfl/projections/k.php?week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    fgm = []
    fga = []
    xp = []

    for i in range(25):
        name = len(str(soup.findAll('td')[0+5*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[0+5*i].findAll('a')[0]).split('>')[1][0:name-3])
        fgm.append(float((str(soup.findAll('td')[1+5*i]).split('>')[1].split('<')[0])))
        fga.append(float((str(soup.findAll('td')[2+5*i]).split('>')[1].split('<')[0])))
        xp.append(float((str(soup.findAll('td')[3+5*i]).split('>')[1].split('<')[0])))

    k_projections = pd.DataFrame({'player_stat':player_stat,'fgm':fgm,'fga':fga,'xp':xp})

    return k_projections
