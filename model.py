import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import timeit
import numpy as np




def add_player(my_team, current_df, name):
    nextplayer = current_df[current_df['player']==name]
    my_team = pd.concat([my_team,nextplayer])
    return my_team

def drop_player(df, name):
    df = df[df['player']!=name]
    return df

def find_player(my_team,df,position):
    test = df[(df['position']==position)]
    bye_list = list(my_team[(my_team['position']==position)]['bye'])
    for i in range(len(bye_list)):
        test = test[test['bye']!=bye_list[i]]
    return test[0:5]

def simulate(my_team,draft_df,simulations):
    current_df = draft_df.copy()
    allpicks = [1,20,21,40,41,60,61,80,81,100,101,120,121,140,141,160]
    roundnum = len(my_team)
    mypicks = (np.array(allpicks)-roundnum*10)[roundnum:17]
    picks = pd.DataFrame(columns=['Rnd1','Rnd2','Rnd3','Rnd4','Rnd5','Rnd6','Rnd7','Rnd8','Rnd9','Rnd10','Rnd11','Rnd12','Rnd13','Rnd14','Rnd15','Rnd16','Pts'],index=range(simulations))
    for i in range(len(my_team)):
        picks.iloc[:,i] = my_team['position'][i]
    currpoints = 0
    runpoints = sum(my_team['points'])
    qb_dict = dict(zip(range(16),[.93,.07,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    rb_dict = dict(zip(range(16),[.80,.80,.60,.30,0,0,0,0,0,0,0,0,0,0,0,0]))
    wr_dict = dict(zip(range(16),[.80,.80,.80,0.80,.30,0,0,0,0,0,0,0,0,0,0,0]))
    te_dict = dict(zip(range(16),[.80,.20,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    dst_dict = dict(zip(range(16),[.93,.07,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    k_dict = dict(zip(range(16),[.93,.07,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    num_qb = sum(my_team['position']=='Q')
    num_rb = sum(my_team['position']=='R')
    num_wr = sum(my_team['position']=='W')
    num_te = sum(my_team['position']=='T')
    num_dst = sum(my_team['position']=='D')
    num_k = sum(my_team['position']=='K')
    qb_bye = list(my_team[my_team['position']=='Q']['bye'])
    rb_bye = list(my_team[my_team['position']=='R']['bye'])
    wr_bye = list(my_team[my_team['position']=='W']['bye'])
    te_bye = list(my_team[my_team['position']=='T']['bye'])
    dst_bye = list(my_team[my_team['position']=='D']['bye'])
    k_bye = list(my_team[my_team['position']=='K']['bye'])
    position_index = []

    start = timeit.default_timer()
    for i in range(len(picks)):
        for j in range((16-roundnum)*10):
            if j not in mypicks:
                bestnum = sorted(current_df['rank'].values)[random.randint(0,2)]
                bestname = current_df[current_df['rank'] == bestnum]['player'].values[0]
                current_df = drop_player(current_df,bestname)
            else:
                if num_qb == 0:
                    position_index.append('Q')
                if ((num_qb == 1) and (roundnum >=9)):
                    position_index.append('Q')
                if num_rb < 3:
                    position_index.append('R')
                if ((num_rb == 3) and (roundnum >=9)):
                    position_index.append('R')
                if num_wr < 4:
                    position_index.append('W')
                if ((num_wr == 4) and (roundnum >=9)):
                    position_index.append('W')
                if num_te == 0:
                    position_index.append('T')
                if ((num_te == 1) and (roundnum >=9)):
                    position_index.append('T')
                if num_dst == 0:
                    position_index.append('D')
                if ((num_dst == 1) and (roundnum >=13)):
                    position_index.append('D')
                if num_k == 0:
                    position_index.append('K')
                if ((num_k == 1) and (roundnum >=13)):
                    position_index.append('K')
                randposition = position_index[random.randint(0,len(position_index)-1)]
                if randposition == 'Q':
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='Q'].iloc[k,4] in qb_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='Q'].iloc[k,1]
                            position = 'Q'
                            currpoints = current_df[current_df['position']=='Q'].iloc[k,7] * qb_dict[num_qb]
                            num_qb += 1
                            qb_bye.append(current_df[current_df['position']=='Q'].iloc[k,4])
                            break
                elif randposition == 'R':
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='R'].iloc[k,4] in rb_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='R'].iloc[k,1]
                            position = 'R'
                            currpoints = current_df[current_df['position']=='R'].iloc[k,7] * rb_dict[num_rb]
                            num_rb += 1
                            rb_bye.append(current_df[current_df['position']=='R'].iloc[k,4])
                            break
                elif randposition == 'W':
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='W'].iloc[k,4] in wr_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='W'].iloc[k,1]
                            position = 'W'
                            currpoints = current_df[current_df['position']=='W'].iloc[k,7] * wr_dict[num_wr]
                            num_wr += 1
                            wr_bye.append(current_df[current_df['position']=='W'].iloc[k,4])
                            break
                elif randposition == 'T':
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='T'].iloc[k,4] in te_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='T'].iloc[k,1]
                            position = 'T'
                            currpoints = current_df[current_df['position']=='T'].iloc[k,7] * te_dict[num_te]
                            num_te += 1
                            te_bye.append(current_df[current_df['position']=='T'].iloc[k,4])
                            break
                elif randposition == 'D':
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='D'].iloc[k,4] in dst_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='D'].iloc[k,1]
                            position = 'DST'
                            currpoints = current_df[current_df['position']=='D'].iloc[k,7] * dst_dict[num_dst]
                            num_dst += 1
                            dst_bye.append(current_df[current_df['position']=='D'].iloc[k,4])
                            break
                else:
                    k = 0
                    while(True):
                        if current_df[current_df['position']=='K'].iloc[k,4] in k_bye:
                            k += 1
                        else:
                            nextplayer = current_df[current_df['position']=='K'].iloc[k,1]
                            position = 'K'
                            currpoints = current_df[current_df['position']=='K'].iloc[k,7] * k_dict[num_k]
                            num_k += 1
                            k_bye.append(current_df[current_df['position']=='K'].iloc[k,4])
                            break
                runpoints += currpoints
                picks.iloc[i,roundnum] = position
                picks.iloc[i,16] = runpoints
                roundnum += 1
                current_df = drop_player(current_df,nextplayer)
                position_index = []
        roundnum = len(my_team)
        currpoints = 0
        runpoints = sum(my_team['points'])
        num_qb = sum(my_team['position']=='Q')
        num_rb = sum(my_team['position']=='R')
        num_wr = sum(my_team['position']=='W')
        num_te = sum(my_team['position']=='T')
        num_dst = sum(my_team['position']=='D')
        num_k = sum(my_team['position']=='K')
        qb_bye = list(my_team[my_team['position']=='Q']['bye'])
        rb_bye = list(my_team[my_team['position']=='R']['bye'])
        wr_bye = list(my_team[my_team['position']=='W']['bye'])
        te_bye = list(my_team[my_team['position']=='T']['bye'])
        dst_bye = list(my_team[my_team['position']=='D']['bye'])
        k_bye = list(my_team[my_team['position']=='K']['bye'])
        current_df = draft_df.copy()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    picks['Pts'] = picks['Pts'].astype(float)
    return(picks.groupby(picks.columns[len(my_team)]).agg({'Pts':['count','min','mean','max']}).round())
