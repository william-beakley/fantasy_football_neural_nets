from __future__ import absolute_import
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import read_data
import drafter
import random
import math

class Team():
    def __init__(self, players, year):
        self.year = year

        self.players_map = {
            "QB": [],
            "WR": [],
            "RB": [],
            "TE": []
        }
        self.players_list = []

        self.players_data = {}
        for player in players:
            self.players_list.append(player)
            self.players_map[read_data.player_position(player, year)].append(player)
            self.players_data[player] = read_data.read_csv_player_all_weeks(player, year)
        

    def call(self):
        totals = []
        for week in range(1, 18):

            qb_scores = [0]
            wr_scores = [0]
            rb_scores = [0]
            te_scores = [0]

            for player in self.players_list:
                player_data = self.players_data[player]
                if player in self.players_map["QB"]:
                    qb_scores.append(round(float(player_data[week][read_data.COLUMN_NAMES_MAP["PPRFantasyPoints"]]), 2))
                elif player in self.players_map["RB"]:
                    rb_scores.append(round(float(player_data[week][read_data.COLUMN_NAMES_MAP["PPRFantasyPoints"]]), 2))
                elif player in self.players_map["WR"]:
                    wr_scores.append(round(float(player_data[week][read_data.COLUMN_NAMES_MAP["PPRFantasyPoints"]]), 2))
                elif player in self.players_map["TE"]:
                    te_scores.append(round(float(player_data[week][read_data.COLUMN_NAMES_MAP["PPRFantasyPoints"]]), 2))
            wr_scores.sort(reverse=True)
            rb_scores.sort(reverse=True)
            flex_scores = wr_scores[2:] + rb_scores[2:]
            total = max(qb_scores) + max(te_scores) + sum(rb_scores[:2]) + sum(wr_scores[:2]) + max(flex_scores)
            totals.append(total)
        return totals

    def print_team(self):
        for key, value in self.players_map.items():
                print(key, ' : ', value)

def head_to_head(t1, t2):
    v1 = np.array(t1)
    v2 = np.array(t2)
    difference = v1 - v2
    w, l, t = 0, 0, 0
    for x in difference:
        if x > 0:
            w += 1
        elif x < 0:
            l += 1
        else:
            t += 1
    return (w, l, t)

def random_schedule(teams, season_length):
    # pick first team's schedule
    # pick second team's schedule out of remaining
    # each team has an id, 0,7
    schedule = []
    for i in range(season_length):
        rand = list(range(teams))
        np.random.shuffle(rand)
        schedule.append(rand)
    return np.array(schedule)


    # for i in range(teams):
    #     count = 0
    #     if i > 0:
    #         for j in range(i):
    #             for k in range(season_length):
    #                 if schedule[j][k] == (i + 1):
    #                     schedule[i][k] = (j + 1)
    #                     count += 1
    #     print(schedule)
    #     repititions = math.ceil((season_length - count)/(teams - i - 1))
    #     weeks = []

    #     for j in range(repititions):
    #         rand = list(range(i + 2, teams + 1))
    #         np.random.shuffle(rand)
    #         weeks = weeks + rand
    #     count_2 = 0
    #     for j in range(season_length):
    #         if schedule[i][j] == 0:
    #             schedule[i][j] = weeks[count_2]
    #             count_2 += 1
    #         else:
    #             print("yeet")
def play_season(totals, schedule):
    teams = 8
    tuples = 4
    schedule_len = len(schedule)
    results = np.zeros([teams, schedule_len])
    for i in range(len(schedule)):
        week = np.reshape(schedule[i], (tuples, 2))
        winner_count =0 
        for t1, t2 in week:

            if totals[t1][i] > totals[t2][i]:
                results[t1][i] = 1
                results[t2][i] = 0
                winner_count +=1 
            elif totals[t1][i] < totals[t2][i]:
                results[t1][i] = 0
                results[t2][i] = 1
                winner_count +=1 
            else: 
                results[t1][i] = 0.5
                results[t2][i] = 0.5
    return results







            
            
                





    




def main():
    # year = input("input year: \n")
    year = "2019"
    players = drafter.read_ADP_CSV(year)
    team_map = drafter.snake_draft(players, 8)
    players_1 = team_map[0]
    players_2 = team_map[1]
    players_3 = team_map[2]
    players_4 = team_map[3]
    players_5 = team_map[4]
    players_6 = team_map[5]
    players_7 = team_map[6]
    players_8 = team_map[7]



    # my_input = input("input players: \n")
    # players = my_input.split(", ")
    team1 = Team(players_1, year)
    team2 = Team(players_2, year)
    team3 = Team(players_3, year)
    team4 = Team(players_4, year)
    team5 = Team(players_5, year)
    team6 = Team(players_6, year)
    team7 = Team(players_7, year)
    team8 = Team(players_8, year)

    totals_1 = team1.call()

    totals_2 = team2.call()

    totals_3 = team3.call()

    totals_4 = team4.call()

    totals_5 = team5.call()

    totals_6 = team6.call()

    totals_7 = team7.call()

    totals_8 = team8.call()
    # print(head_to_head(totals_1, totals_2))
    # print(head_to_head(totals_3, totals_4))
    # print(head_to_head(totals_5, totals_6))
    # print(head_to_head(totals_7, totals_8))
    wins = np.zeros([8])
    for i in range(100):
        schedule = random_schedule(8, 16)
        results = play_season([totals_1, totals_2, totals_3, totals_4, totals_5, totals_6, totals_7, totals_8], schedule)
        vec = np.sum(results, axis=1)
        wins += vec
    print(wins/100)




    return


if __name__ == '__main__':
    main()
