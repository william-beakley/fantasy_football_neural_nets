import csv
from os import read
import numpy as np

COLUMN_NAMES = ['Player', 'Pos', 'Tm', 'PassingYds', 'PassingTD', 'Int', 'PassingAtt',
'Cmp', 'RushingAtt', 'RushingYds', 'RushingTD', 'Rec', 'Tgt', 'ReceivingYds',
'ReceivingTD', 'FL', 'PPRFantasyPoints', 'StandardFantasyPoints', 'HalfPPRFantasyPoints']
COLUMN_NAMES_MAP = {
    'Player': 0,
    'Pos': 1,
    'Tm' : 2, 
    'PassingYds': 3, 
    'PassingTD': 4, 
    'Int': 5, 
    'PassingAtt': 6,
    'Cmp': 7, 
    'RushingAtt': 8, 
    'RushingYds': 9,
    'RushingTD': 10,
    'Rec': 11, 
    'Tgt': 12, 
    'ReceivingYds': 13, 
    'ReceivingTD': 14, 
    'FL' : 15, 
    'PPRFantasyPoints': 16, 
    'StandardFantasyPoints': 17, 
    'HalfPPRFantasyPoints': 18
    }

RELEVANT_CATEGORIES_MAP = {
    "QB" : [3, 4, 5, 6, 7, 8, 9, 10, 15, 16],
    "WR" : [11, 12, 13, 14, 15, 16],
    "RB" : [8, 9, 10, 11, 12, 13, 14, 15, 16],
    "TE" : [11, 12, 13, 14, 15, 16]
}


def read_csv_player_week(name, year, week):
    with open("data/weekly/" + year + "/week" + week + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if(name.lower() == (row[0]).lower()):
                print_week(row)

def read_csv_player_all_weeks(name, year):
    player_data = {}
    played = []
    for week in range(1,18):
        with open("data/weekly/" + year + "/week" + str(week) + ".csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            found = False
            for row in spamreader:
                if((row[0]).lower() in name.lower() or name.lower() in (row[0]).lower()):
                    player_data[week] = row
                    found = True
                    played.append(week)
                    break
            if (not found):
                player_data[week] = list(np.zeros(19))
    player_data["played"] = played

            
            
    return player_data

def scores_for_year(name, year):
    player_data = np.zeros([17])
    for week in range(1,18):
        with open("data/weekly/" + year + "/week" + str(week) + ".csv", newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if((row[0]).lower() in name.lower() or name.lower() in (row[0]).lower()):
                    player_data[week - 1] = row[16]
                    break
    return player_data

def all_players_scores_week(year, week, player_map):
    keys = player_map.keys()
    num_keys = len(keys)
    with open("data/weekly/" + year + "/week" + week + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        scores = np.zeros([num_keys + 1])
        for row in spamreader:
            name = (row[0]).lower()
            if name in keys:
                scores[player_map[name]] = row[16]
        return scores

                

def all_players_scores_year(year):
    player_map = {}
    with open("data/yearly/" + str(year) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = -1
        for row in spamreader:
            if i == -1:
                i += 1
            elif row[3] != "0":
                player_map[(row[1]).lower()] = i
                i += 1
    scores = []
    for week in range(1,18):
        scores.append(all_players_scores_week(str(year), str(week), player_map))
    npscores = np.array(scores)
    trans = np.transpose(npscores)

    return trans


# def print_week(row):
#     for i in range(len(row)):
#         print(COLUMN_NAMES[i] + ": " + row[i])

def print_week(row):
    for i in RELEVANT_CATEGORIES_MAP[row[1]]:
        print(COLUMN_NAMES[i] + ": " + row[i])

def player_week():
    while(True):
        my_input = input("player, year, week: \n")
        name, year, week = my_input.split(", ")
        read_csv_player_week(name, year, week)

def average_across_weeks(player_data, category):
    col_num = COLUMN_NAMES_MAP[category]
    values = []
    for week in range(1, 18):
        val = round(float(player_data[week][col_num]), 2)
        values.append(val)
        print(val)
    print("avg: " + str(sum(values)/len(player_data["played"])))
        

def player_all_weeks():
        while(True):
            my_input = input("player, year: \n")
            name, year = my_input.split(", ")
            player_data = read_csv_player_all_weeks(name, year)
            category = input("which category: \n")
            average_across_weeks(player_data, category)

def player_position(name, year):
    with open("data/yearly/" + year + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if(name.lower() == (row[1]).lower()):
                return row[3]

    
            
# my_input = input("week or year: \n")
# if my_input == "week":
#     player_week()
# elif my_input == "year":
#     player_all_weeks()
scores = all_players_scores_year(2019)
print(scores.shape)
