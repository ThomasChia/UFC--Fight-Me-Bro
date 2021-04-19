"""
Created on Mon Dec 28 2020

@author: Thomas Chia

Description: Take in preprocessed dataset, fill in missing values, create features, and double the rows.
The goal is to create a new dataset from this where ML algorithms can be used.

Order:
1. Calculate ELO rankings based on winners and losers and add to dataframe
2. Sort cumulative data, like total time and lifetime strikes
3. Double the rows so that each entry represents a single result
4. Add physical statistics, such as height and weight
"""

from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

address = 'Odds_Data/fight_data_odds_2.csv'
df = pd.read_csv(address)
df = df[::-1]
df = df.reset_index()
df = df.drop(['Unnamed: 0', 'index'], axis=1)
print(df.head())

address = 'fighter_data_clean.csv'
df_stats = pd.read_csv(address)
df_stats = df_stats.drop(['Unnamed: 0'], axis=1)
print(df_stats.head())


def create_elo(data):
    """
    Given the list on matches in chronological order, for each match, computes
    the elo ranking of the 2 fighters at the beginning of the match

    """
    print("Elo rankings computing...")
    fighters = list(pd.Series(list(data.Winner) + list(data.Loser)).value_counts().index)
    elo = pd.Series(np.ones(len(fighters)) * 1500, index=fighters)
    print(elo)
    print('Number of fighters is:', len(elo))
    ranking_elo = [(1500, 1500)]
    for i in range(1, len(data)):
        w = data.iloc[i - 1, :].Winner
        l = data.iloc[i - 1, :].Loser
        elow = elo[w]
        elol = elo[l]
        pwin = 1 / (1 + 10 ** ((elol - elow) / 400))
        K_win = 32
        K_los = 32
        new_elow = elow + K_win * (1 - pwin)
        new_elol = elol - K_los * (1 - pwin)
        elo[w] = new_elow
        elo[l] = new_elol
        ranking_elo.append((elo[data.iloc[i - 1, :].Winner], elo[data.iloc[i - 1, :].Loser]))
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    ranking_elo = pd.DataFrame(ranking_elo, columns=["elo_winner", "elo_loser"])
    ranking_elo["proba_elo"] = 1 / (1 + 10 ** ((ranking_elo["elo_loser"] - ranking_elo["elo_winner"]) / 400))
    return ranking_elo


def add_fighters_elo(data):
    """
    Given the list on matches in chronological order, for each match, computes
    the elo ranking of the 2 fighters at the beginning of the match

    """
    data['eloW'] = ''
    data['eloL'] = ''
    # this creates two extra columns for the elo stats BEFORE the fight to be entered
    print("Elo rankings computing...")
    fighters = list(pd.Series(list(data.Winner) + list(data.Loser)).value_counts().index)
    elo = pd.Series(np.ones(len(fighters)) * 1500, index=fighters)
    # elo is an initial list of all fighters, giving them all a score of 1500
    print(elo)
    print('Number of fighters is:', len(elo))
    ranking_elo = [(1500, 1500)]
    for i in range(1, len(data) + 1):
        w = data.iloc[i - 1, :].Winner
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i - 1, :].Loser
        # l is the name of the losing fighter for a given row
        # data.iloc[i - 1, :]['eloW'] = elo[w]
        # data.iloc[i - 1, :]['eloL'] = elo[l]
        data.iloc[i - 1, data.columns.get_loc('eloW')] = elo[w]
        data.iloc[i - 1, data.columns.get_loc('eloL')] = elo[l]
        # assigning the elo values to each fighter BEFORE the fight
        elow = elo[w]
        # print(elow)
        # elow is the elo score of the winning fighter BEFORE the fight
        elol = elo[l]
        # elol is the elo score of the losing fighter BEFORE the fight
        pwin = 1 / (1 + 10 ** ((elol - elow) / 400))
        # pwin is the probability of the winner winning using the existing elo scores of both of the fighters (probability BEFORE the fight)
        K_win = 32
        K_los = 32
        new_elow = elow + K_win * (1 - pwin)
        new_elol = elol - K_los * (1 - pwin)
        # these two formulas calculate the new elo scores for the winner and the loser based on the outcome of the match
        elo[w] = new_elow
        elo[l] = new_elol
        # this updates the series of elo scores of fighters for the winner and the loser with the newly calculated scores
        ranking_elo.append((elo[data.iloc[i - 1, :].Winner], elo[data.iloc[i - 1, :].Loser]))
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    ranking_elo = pd.DataFrame(ranking_elo, columns=["elo_winner", "elo_loser"])
    ranking_elo["proba_elo"] = 1 / (1 + 10 ** ((ranking_elo["elo_loser"] - ranking_elo["elo_winner"]) / 400))
    return ranking_elo, data


def add_fighters_elo_penalty(data):
    """
    Given the list on matches in chronological order, for each match, computes
    the elo ranking of the 2 fighters at the beginning of the match

    """
    data['eloW'] = ''
    data['eloL'] = ''
    print("Elo rankings computing...")
    fighters = list(pd.Series(list(data.Winner) + list(data.Loser)).value_counts().index)
    elo = pd.Series(np.ones(len(fighters)) * 1500, index=fighters)
    no_fights = pd.Series(np.zeros(len(fighters)), index=fighters)
    # print(no_fights)
    # print(elo)
    print('Number of fighters is:', len(elo))
    ranking_elo = [(1500, 1500)]
    for i in range(1, len(data) + 1):
        w = data.iloc[i - 1, :].Winner
        # w is the name of the winning fighter for a given row
        l = data.iloc[i - 1, :].Loser
        # l is the name of the losing fighter for a given row
        data.iloc[i - 1, data.columns.get_loc('eloW')] = elo[w]
        data.iloc[i - 1, data.columns.get_loc('eloL')] = elo[l]
        # assigning the elo values to each fighter BEFORE the fight
        elow = elo[w]
        # print(elow)
        # elow is the elo score of the winning fighter BEFORE the fight
        elol = elo[l]
        # elol is the elo score of the losing fighter BEFORE the fight
        no_fights[w] += 1
        no_fights[l] += 1
        # this counts the number of fights that each fighter has had in the UFC so far
        pwin = 1 / (1 + 10 ** ((elol - elow) / 400))
        # pwin is the probability of the winner winning using the existing elo scores of both of the fighters (probability BEFORE the fight)
        K_win = 32
        K_los = 32
        # new_elow = elow + K_win * (1 - pwin) / no_fights[w]
        # new_elol = elol - K_los * (1 - pwin) / no_fights[l]
        new_elow = elow + K_win * (1 - pwin)
        new_elol = elol - K_los * (1 - pwin)
        # these two formulas calculate the new elo scores for the winner and the loser based on the outcome of the match
        # this adds a penalty for the number of fights that a fighter has as it is assumed that more fights cause more damage and so result in poorer future performance
        # HYPOTHESIS this can be tested with a linear regression
        elo[w] = new_elow
        elo[l] = new_elol
        # print(elo[w])
        # this updates the series of elo scores of fighters for the winner and the loser with the newly calculated scores
        # print(ranking_elo)
        # print(elo[data.iloc[i, :].Winner])
        # ranking_elo.append((elo[data.iloc[i, :].Winner], elo[data.iloc[i, :].Loser]))
        ranking_elo.append((elo[data.iloc[i - 1, :].Winner], elo[data.iloc[i - 1, :].Loser]))
        # ranking elo is a list of elo scores. The new scores from the last fight are added. But it actually looks like this is appending the elo score of the next player!!!! BUT why is the first row set at 1500 1500
        # I imagine that this is tied into why it it i and not i-1 that is updated perhaps?
        # print(ranking_elo)
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    ranking_elo = pd.DataFrame(ranking_elo, columns=["elo_winner", "elo_loser"])
    ranking_elo["proba_elo"] = 1 / (1 + 10 ** ((ranking_elo["elo_loser"] - ranking_elo["elo_winner"]) / 400))
    return ranking_elo, data


def calc_prediction_pct(row):
    if row['elo_winner'] > row['elo_loser']:
        return 1
    elif row['elo_winner'] < row['elo_loser']:
        return 0
    else:
        return 0
        # return 0.5


def calc_past_record(data):
    data['past_W_F'] = ''
    data['past_L_F'] = ''
    data['past_W_O'] = ''
    data['past_L_O'] = ''
    print("Calculating past record...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_W = pd.Series(np.zeros(len(fighters)), index=fighters)
    no_L = pd.Series(np.zeros(len(fighters)), index=fighters)
    j = 0
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('past_W_F')] = no_W[w]
        # past wins, fighter
        data.iloc[i, data.columns.get_loc('past_L_O')] = no_L[l]
        # past losses, opponent
        data.iloc[i, data.columns.get_loc('past_L_F')] = no_L[w]
        # past losses, fighter
        data.iloc[i, data.columns.get_loc('past_W_O')] = no_W[l]
        # past wins, opponent
        no_KD_F = no_W[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_KD_O = no_L[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        no_W[w] += 1
        no_L[l] += 1
        # this adds a win and a loss from the fight scored by each fighter
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def calc_past_record_pct(data):
    data['past_W_%_F'] = ''
    data['past_L_%_F'] = ''
    data['past_W_%_O'] = ''
    data['past_L_%_O'] = ''
    print("Calculating past record...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_W = pd.Series(np.zeros(len(fighters)), index=fighters)
    no_L = pd.Series(np.zeros(len(fighters)), index=fighters)
    j = 0
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        try:
            data.iloc[i, data.columns.get_loc('past_W_%_F')] = no_W[w] / (no_W[w] + no_L[w])
        except ZeroDivisionError:
            data.iloc[i, data.columns.get_loc('past_W_%_F')] = 0.5
        # past wins, fighter
        try:
            data.iloc[i, data.columns.get_loc('past_L_%_O')] = no_L[l] / (no_W[l] + no_L[l])
        except ZeroDivisionError:
            data.iloc[i, data.columns.get_loc('past_L_%_O')] = 0.5
        # past losses, opponent
        try:
            data.iloc[i, data.columns.get_loc('past_L_%_F')] = no_L[w] / (no_W[w] + no_L[w])
        except ZeroDivisionError:
            data.iloc[i, data.columns.get_loc('past_L_%_F')] = 0.5
        # past losses, fighter
        try:
            data.iloc[i, data.columns.get_loc('past_W_%_O')] = no_W[l] / (no_W[l] + no_L[l])
        except ZeroDivisionError:
            data.iloc[i, data.columns.get_loc('past_W_%_O')] = 0.5
        # past wins, opponent
        no_KD_F = no_W[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_KD_O = no_L[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        no_W[w] += 1
        no_L[l] += 1
        # this adds a win and a loss from the fight scored by each fighter
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def calc_past_stats(data, column_a, column_b):
    data['past_{}'.format(column_a)] = ''
    data['past_{}'.format(column_b)] = ''
    print("Calculating past statistics...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_KD = pd.Series(np.zeros(len(fighters)), index=fighters)
    j = 0
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('past_{}'.format(column_a))] = no_KD[w]
        data.iloc[i, data.columns.get_loc('past_{}'.format(column_b))] = no_KD[l]
        # assigning the KD values to each fighter BEFORE the fight
        no_KD_F = no_KD[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_KD_O = no_KD[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        new_KD_W = data.iloc[i, data.columns.get_loc(column_a)]
        new_KD_L = data.iloc[i, data.columns.get_loc(column_b)]
        # print(new_KD_W)
        # print(j)
        j += 1
        try:
            no_KD[w] = no_KD_F + int(float(new_KD_W))
        except ValueError:
            no_KD[w] = no_KD_F + 0
        try:
            no_KD[l] = no_KD_O + int(float(new_KD_L))
        except ValueError:
            no_KD[l] = no_KD_O + 0
        # this adds on the number of KD from the fight scored by each fighter

        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def add_round_perf(data, column):
    data['past_{}_F'.format(column)] = ''
    data['past_{}_O'.format(column)] = ''
    print("Calculating past round, and performance statistics...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_rounds = pd.Series(np.zeros(len(fighters)), index=fighters)
    j = 0
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('past_{}_F'.format(column))] = no_rounds[w]
        data.iloc[i, data.columns.get_loc('past_{}_O'.format(column))] = no_rounds[l]
        # assigning the KD values to each fighter BEFORE the fight
        no_rounds_F = no_rounds[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_rounds_O = no_rounds[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        new_rounds_W = data.iloc[i, data.columns.get_loc(column)]
        new_rounds_L = data.iloc[i, data.columns.get_loc(column)]
        # print(new_KD_W)
        # print(j)
        j += 1
        try:
            no_rounds[w] = no_rounds_F + int(float(new_rounds_W))
        except ValueError:
            no_rounds[w] = no_rounds_F + 0
        try:
            no_rounds[l] = no_rounds_O + int(float(new_rounds_L))
        except ValueError:
            no_rounds[l] = no_rounds_O + 0
        # this adds on the number of KD from the fight scored by each fighter

        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def add_time(data):
    # data['TIME'] = pd.to_datetime(data['TIME'], format = '%M:%S')
    data['TIME'] = data['TIME'].astype(str)
    data['past_TIME_F'] = ''
    data['past_TIME_O'] = ''
    print("Calculating past time statistics...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_rounds = pd.Series(np.empty(len(fighters)), index=fighters, dtype=np.str)
    no_rounds.values[:] = '0:0:0'
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('past_TIME_F')] = no_rounds[w]
        data.iloc[i, data.columns.get_loc('past_TIME_O')] = no_rounds[l]
        # assigning the KD values to each fighter BEFORE the fight
        no_rounds_F = no_rounds[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_rounds_O = no_rounds[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        new_rounds_F = data.iloc[i, data.columns.get_loc('TIME')]
        new_rounds_O = data.iloc[i, data.columns.get_loc('TIME')]
        # print(type(new_rounds_O))
        # print(new_rounds_O)
        # print(type(str(no_rounds_F)))
        # print(no_rounds_F)
        # print(str(no_rounds_F).split(':'))
        (h_F, m_F, s_F) = str(no_rounds_F).split(':')
        (m_F_new, s_F_new) = str(new_rounds_F).split(':')
        (h_O, m_O, s_O) = str(no_rounds_O).split(':')
        (m_O_new, s_O_new) = str(new_rounds_O).split(':')
        try:
            # no_rounds[w] = no_rounds_F + timedelta(new_rounds_F)
            no_rounds[w] = timedelta(hours=int(h_F), minutes=int(m_F), seconds=int(s_F)) + timedelta(
                minutes=int(m_F_new), seconds=int(s_F_new))
        except ValueError:
            no_rounds[w] += 0
        try:
            # no_rounds[l] = no_rounds_O + timedelta(new_rounds_O)
            no_rounds[l] = timedelta(hours=int(h_O), minutes=int(m_O), seconds=int(s_O)) + timedelta(
                minutes=int(m_O_new), seconds=int(s_O_new))
        except ValueError:
            no_rounds[l] += 0
        # this adds on the number of KD from the fight scored by each fighter

        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def add_seconds(data):
    # data['TIME'] = pd.to_datetime(data['TIME'], format = '%M:%S')
    data['TIME'] = data['TIME'].astype(str)
    data['past_SECONDS_F'] = ''
    data['past_SECONDS_O'] = ''
    print("Calculating past seconds statistics...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    no_rounds = pd.Series(np.zeros(len(fighters)), index=fighters)
    # no_rounds.values[:] = '0'
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # print(w)
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('past_SECONDS_F')] = no_rounds[w]
        data.iloc[i, data.columns.get_loc('past_SECONDS_O')] = no_rounds[l]
        # assigning the KD values to each fighter BEFORE the fight
        no_rounds_F = no_rounds[w]
        # no_KD_F is the KD's of the winning fighter BEFORE the fight
        no_rounds_O = no_rounds[l]
        # no_KD_O is the KD's of the losing fighter BEFORE the fight
        new_rounds_F = data.iloc[i, data.columns.get_loc('TIME')]
        new_rounds_O = data.iloc[i, data.columns.get_loc('TIME')]
        # print(type(new_rounds_O))
        # print(new_rounds_O)
        # print(type(str(no_rounds_F)))
        # print(no_rounds_F)
        # print(str(no_rounds_F).split(':'))
        # (h_F, m_F, s_F) = str(no_rounds_F).split(':')
        (m_F_new, s_F_new) = str(new_rounds_F).split(':')
        # (h_O, m_O, s_O) = str(no_rounds_O).split(':')
        (m_O_new, s_O_new) = str(new_rounds_O).split(':')
        try:
            # no_rounds[w] = no_rounds_F + timedelta(new_rounds_F)
            no_rounds[w] = int(m_F_new) * 60 + int(s_F_new) + no_rounds_F
        except ValueError:
            no_rounds[w] += 0
        try:
            # no_rounds[l] = no_rounds_O + timedelta(new_rounds_O)
            no_rounds[l] = int(m_O_new) * 60 + int(s_O_new) + no_rounds_O
        except ValueError:
            no_rounds[l] += 0
        # this adds on the number of KD from the fight scored by each fighter

        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def double_rows(data):
    data = data.reset_index()
    data_copy = data.copy()

    # columns_ = {'Date': 'Date', 'Winner': 'Fighter', 'Loser': 'Opponent', 'KD_W': 'KD_F', 'KD_L': 'KD_O', 'STR_W': 'STR_F',
    #             'STR_L': 'STR_O', 'TD_W': 'TD_F', 'TD_L': 'TD_O', 'SUB_W': 'SUB_F', 'SUB_L': 'SUB_O',
    #             'WEIGHT CLASS': 'WEIGHT CLASS', 'PERF': 'PERF', 'FINISH': 'FINISH', 'METHOD': 'METHOD',
    #             'ROUND': 'ROUND', 'TIME': 'TIME', 'eloW': 'elo_F', 'eloL': 'elo_O'}

    data_copy['Fighter'] = data['Opponent']
    data_copy['Opponent'] = data['Fighter']
    data_copy['past_KD_F'] = data['past_KD_O']
    data_copy['past_KD_O'] = data['past_KD_F']
    data_copy['elo_F'] = data['elo_O']
    data_copy['elo_O'] = data['elo_F']
    data_copy['past_STR_F'] = data['past_STR_O']
    data_copy['past_STR_O'] = data['past_STR_F']
    data_copy['past_TD_F'] = data['past_TD_O']
    data_copy['past_TD_O'] = data['past_TD_F']
    data_copy['past_SUB_F'] = data['past_SUB_O']
    data_copy['past_SUB_O'] = data['past_SUB_F']
    data_copy['past_W_F'] = data['past_W_O']
    data_copy['past_L_F'] = data['past_L_O']
    data_copy['past_W_O'] = data['past_W_F']
    data_copy['past_L_O'] = data['past_L_F']
    data_copy['past_W_%_F'] = data['past_W_%_O']
    data_copy['past_L_%_F'] = data['past_L_%_O']
    data_copy['past_W_%_O'] = data['past_W_%_F']
    data_copy['past_L_%_O'] = data['past_L_%_F']
    data_copy['past_ROUND_O'] = data['past_ROUND_F']
    data_copy['past_ROUND_F'] = data['past_ROUND_O']
    data_copy['past_PERF_O'] = data['past_PERF_F']
    data_copy['past_PERF_F'] = data['past_PERF_O']
    data_copy['past_TIME_O'] = data['past_TIME_F']
    data_copy['past_TIME_F'] = data['past_TIME_O']
    data_copy['past_SECONDS_O'] = data['past_SECONDS_F']
    data_copy['past_SECONDS_F'] = data['past_SECONDS_O']
    data_copy['Ht_O'] = data['Ht_F']
    data_copy['Ht_F'] = data['Ht_O']
    data_copy['Wt_F'] = data['Wt_O']
    data_copy['Wt_O'] = data['Wt_F']
    data_copy['Reach_F'] = data['Reach_O']
    data_copy['Reach_O'] = data['Reach_F']
    data_copy['Stance_F'] = data['Stance_O']
    data_copy['Stance_O'] = data['Stance_F']
    data_copy['days_since_last_fight_F'] = data['days_since_last_fight_O']
    data_copy['days_since_last_fight_O'] = data['days_since_last_fight_F']
    data_copy['average_odds_F'] = data['average_odds_O']
    data_copy['average_odds_O'] = data['average_odds_F']

    data['Outcome'] = 1
    data_copy['Outcome'] = 0

    ### This is to not have double entries, but still have a mix of wins and losses
    # data_values = []
    # copy_values = []
    # for i in range(0, len(data.index) - 1, 2):
    #         data_values.append(i)
    #         copy_values.append(i + 1)
    #
    # data = data.drop(data_values, axis = 0)
    # data_copy = data_copy.drop(copy_values, axis = 0)

    ### This is the end of this section.

    data_double = data.append(data_copy)
    data_double.sort_values(by=['index'], inplace=True)
    print(data_double.head())
    # change data rows from winner to fighter, loser to opponent etc
    # do same but the opposite for df
    # join the rows
    # sort based on the index column, so they will hopefully be in order
    return data_double


def create_differences(data):
    data['TD_dif'] = data['past_TD_F'] - data['past_TD_O']
    data['KD_dif'] = data['past_KD_F'] - data['past_KD_O']
    data['SUB_dif'] = data['past_SUB_F'] - data['past_SUB_O']
    data['STR_dif'] = data['past_STR_F'] - data['past_STR_O']
    data['WT_dif'] = data['Wt_F'] - data['Wt_O']
    data['HT_dif'] = data['Ht_F'] - data['Ht_O']
    data['REACH_dif'] = data['Reach_F'] - data['Reach_O']
    data['ELO_dif'] = data['elo_F'] - data['elo_O']
    data['Days_dif'] = data['days_since_last_fight_F'] - data['days_since_last_fight_O']
    data['Rounds_dif'] = data['past_ROUND_F'] - data['past_ROUND_O']
    data['Perf_of_Night_dif'] = data['past_PERF_F'] - data['past_PERF_O']
    data['Seconds_in_Ring_dif'] = data['past_SECONDS_F'] - data['past_SECONDS_O']
    data['Win_dif'] = data['past_W_F'] - data['past_W_O']
    data['Loss_dif'] = data['past_L_F'] - data['past_L_O']

    return data


def add_per_min_stats(data):
    data['TD_per_min'] = (data['past_TD_F'] / data['past_SECONDS_F']) * 60
    data['KD_per_min'] = (data['past_KD_F'] / data['past_SECONDS_F']) * 60
    data['SUB_per_min'] = (data['past_SUB_F'] / data['past_SECONDS_F']) * 60
    data['STR_per_min'] = (data['past_STR_F'] / data['past_SECONDS_F']) * 60

    return data


def add_days_since_last(data):
    data['Date'] = pd.to_datetime(data['Date'])

    data['days_since_last_fight_F'] = ''
    data['days_since_last_fight_O'] = ''
    print("Calculating days since last fight...")
    fighters = list(pd.Series(list(data.Fighter) + list(data.Opponent)).value_counts().index)
    date_of_last_fight = pd.Series(np.zeros(len(fighters)), index=fighters)
    date_of_last_fight = pd.to_datetime(date_of_last_fight)
    date_of_last_fight.values[:] = data['Date'][0]
    for i in range(0, len(data)):
        w = data.iloc[i, :].Fighter
        # w is the name of the winning fighter for a given row
        l = data.iloc[i, :].Opponent
        # l is the name of the losing fighter for a given row
        data.iloc[i, data.columns.get_loc('days_since_last_fight_F')] = (data.iloc[i, data.columns.get_loc('Date')]
                                                                         - date_of_last_fight[w]).days
        # days since winners last fight
        data.iloc[i, data.columns.get_loc('days_since_last_fight_O')] = (data.iloc[i, data.columns.get_loc('Date')]
                                                                         - date_of_last_fight[l]).days
        # days since losers last fight
        date_of_last_fight[w] = data.iloc[i, data.columns.get_loc('Date')]
        date_of_last_fight[l] = data.iloc[i, data.columns.get_loc('Date')]
        # this adds the date of the last fight to the series of latest fight dates from each fighter.
        if i % 5000 == 0:
            print(str(i) + " matches computed...")
    print(data.head())

    return data


def add_fighter_stats(data_main, data_physical):
    # data_physical['Ht.']

    data_physical['Fighter'] = data_physical['First'] + ' ' + data_physical['Last']
    data_physical_key = data_physical.drop(['Nickname', 'W', 'L', 'D', 'Belt', 'First', 'Last'], axis=1)
    print(data_physical_key)
    data_return = data_main.merge(data_physical_key, on='Fighter', how='left')

    columns_ = {'Ht.': 'Ht_F', 'Wt.': 'Wt_F', 'Reach': 'Reach_F',
                'Stance': 'Stance_F'}
    data_return = data_return.rename(columns=columns_)

    columns_O = {'Fighter': 'Opponent'}
    data_physical_key = data_physical_key.rename(columns=columns_O)
    data_return = data_return.merge(data_physical_key, on='Opponent', how='left')

    columns_ = {'Ht.': 'Ht_O', 'Wt.': 'Wt_O', 'Reach': 'Reach_O',
                'Stance': 'Stance_O'}
    data_return = data_return.rename(columns=columns_)

    return data_return


def move_unique(data):
    data = data.drop('index')
    data_2 = data.dropna(subset = ['average_odds_F'])
    print(data_2.head())
    data_2 = data_2.reset_index()
    data_2 = data_2.drop('level_0', axis = 1)
    data_2 = data_2.reset_index()
    print(data_2.head())
    first_index = []
    first_fighter = []
    repeat_index = []
    repeat_fighter = []

    for i in range(0, len(data_2)):
        fighter = data_2['Fighter'][i]
        # print(i)
        # print(fighter)
        if fighter not in first_fighter:
            first_index.append(data_2['level_0'][i])
            first_fighter.append(data_2['Fighter'][i])
        else:
            repeat_index.append(data_2['level_0'][i])
            repeat_fighter.append(data_2['Fighter'][i])

    full = first_index + repeat_index
    print(full)

    data_2 = data_2.reindex(full)

    return data_2


##### TESTER CODE #####

# elo_ = create_elo(df)
# print(elo_)
# print('Number of elo rankings:', len(elo_))
# print(df.head())

# elo, df_elo = add_fighters_elo(df)
# print(df_elo.head())
# df_elo.to_csv('fighter_data_elo.csv')

# data_return = add_fighter_stats(df, df_stats)
# print(data_return)
# This will add the height, weight, etc stats from the fighter_data.csv file


##### REAL CODE #####

elo, df_elo = add_fighters_elo_penalty(df)
print(df_elo.head())
# df_elo.to_csv('fighter_data_elo_penalty.csv')


elo['pred correct'] = elo.apply(calc_prediction_pct, axis=1)
correct_pct = elo['pred correct'].sum() / len(elo['pred correct'])
print(correct_pct * 100)

columns_ = {'Date': 'Date', 'Winner': 'Fighter', 'Loser': 'Opponent',
            'KD_W': 'KD_F', 'KD_L': 'KD_O', 'STR_W': 'STR_F',
            'STR_L': 'STR_O', 'TD_W': 'TD_F', 'TD_L': 'TD_O', 'SUB_W': 'SUB_F', 'SUB_L': 'SUB_O',
            'WEIGHT CLASS': 'WEIGHT CLASS', 'PERF': 'PERF', 'FINISH': 'FINISH', 'METHOD': 'METHOD',
            'ROUND': 'ROUND', 'TIME': 'TIME', 'eloW': 'elo_F', 'eloL': 'elo_O'}
df_elo = df_elo.rename(columns=columns_)

df_elo = calc_past_record(df_elo)
df_elo = calc_past_record_pct(df_elo)
df_elo = add_fighter_stats(df_elo, df_stats)
df_elo = calc_past_stats(df_elo, 'KD_F', 'KD_O')
df_elo = calc_past_stats(df_elo, 'STR_F', 'STR_O')
df_elo = calc_past_stats(df_elo, 'TD_F', 'TD_O')
df_elo = calc_past_stats(df_elo, 'SUB_F', 'SUB_O')
df_elo = add_round_perf(df_elo, 'ROUND')
df_elo = add_round_perf(df_elo, 'PERF')
df_elo = add_time(df_elo)
df_elo = add_seconds(df_elo)
df_elo = add_days_since_last(df_elo)

df_elo_stats = double_rows(df_elo)
df_elo_stats = create_differences(df_elo_stats)
df_elo_stats = add_per_min_stats(df_elo_stats)
# df_elo_stats = move_unique(df_elo_stats)
print(df_elo_stats.head())
df_elo_stats.to_csv('fighter_data_final_v14.csv')

# data_stats = add_fighter_stats(df_elo_double, df_stats)
