import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import timeit
import numpy as np


def get_scoring_dict():
    scoring_dict = {'passing_yards_score':0.04,
    'passing_TD_score':4,
    'passing_interception_score':-2,
    'rushing_yards_score':0.1,
    'rushing_TD_score':6,
    'offense_fumble_score':-2,
    'receptions_score':0,
    'receiving_yards_score':0.1,
    'receiving_TD_score':6,
    'sack_score':1,
    'defense_interception_score':2,
    'defense_fumble_score':2,
    'defense_TD_score':6,
    'safety_score':2,
    'points_against_score':-2/7,
    'fg_made_score':4,
    'fg_miss_score':-1,
    'xp_made_score':1,
    'xp_miss_score':-1}

    return scoring_dict

def qb_scoring(qb_projections, scoring_dict):
    qb_projections['points'] = qb_projections['yards'] * scoring_dict['passing_yards_score'] + qb_projections['touchdowns'] * scoring_dict['passing_TD_score'] +\
    qb_projections['interceptions'] * scoring_dict['passing_interception_score'] + qb_projections['rush_yards'] * scoring_dict['rushing_yards_score'] +\
    qb_projections['rush_tds'] * scoring_dict['rushing_TD_score'] + qb_projections['fumbles'] * scoring_dict['offense_fumble_score']

    return qb_projections

def rb_scoring(rb_projections, scoring_dict):
    rb_projections['points'] = rb_projections['rush_yards'] * scoring_dict['rushing_yards_score'] + rb_projections['rush_tds'] * scoring_dict['rushing_TD_score'] +\
    rb_projections['receptions'] * scoring_dict['receptions_score'] + rb_projections['receive_yards'] * scoring_dict['receiving_yards_score'] +\
    rb_projections['receive_tds'] * scoring_dict['receiving_TD_score'] + rb_projections['fumbles'] * scoring_dict['offense_fumble_score']

    return rb_projections

def wr_scoring(wr_projections, scoring_dict):
    wr_projections['points'] = wr_projections['rush_yards'] * scoring_dict['rushing_yards_score'] + wr_projections['rush_tds'] * scoring_dict['rushing_TD_score'] +\
    wr_projections['receptions'] * scoring_dict['receptions_score'] + wr_projections['receive_yards'] * scoring_dict['receiving_yards_score'] +\
    wr_projections['receive_tds'] * scoring_dict['receiving_TD_score'] + wr_projections['fumbles'] * scoring_dict['offense_fumble_score']

    return wr_projections

def te_scoring(te_projections, scoring_dict):
    te_projections['points'] = te_projections['receptions'] * scoring_dict['receptions_score'] +\
    te_projections['receive_yards'] * scoring_dict['receiving_yards_score'] + te_projections['receive_tds'] * scoring_dict['receiving_TD_score'] +\
    te_projections['fumbles'] * scoring_dict['offense_fumble_score']

    return te_projections

def dst_scoring(dst_projections, scoring_dict):
    dst_projections['points'] = dst_projections['sack'] * scoring_dict['sack_score'] + dst_projections['interception'] * scoring_dict['defense_interception_score'] +\
    dst_projections['fumble_recovered'] * scoring_dict['defense_fumble_score'] + dst_projections['touchdowns'] * scoring_dict['defense_TD_score'] +\
    dst_projections['safety'] * scoring_dict['safety_score'] + dst_projections['points_against'] * scoring_dict['points_against_score'] + 7

    return dst_projections

def k_scoring(k_projections, scoring_dict):
    k_projections['points'] = k_projections['fgm'] * scoring_dict['fg_made_score'] + (k_projections['fga'] - k_projections['fgm']) * scoring_dict['fg_miss_score'] +\
    k_projections['xp'] * scoring_dict['xp_made_score'] + k_projections['xp'] * .05 * scoring_dict['xp_miss_score']

    return k_projections
