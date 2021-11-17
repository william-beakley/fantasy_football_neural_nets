import csv

from numpy.core.numeric import Infinity

POSITIONS = ["QB", "RB", "WR", "TE"]
POSITIONS_MAP = {
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3
}
def read_ADP_CSV(year):
    players = []
    with open("data/ADP/" + year + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[3] in POSITIONS:
                players.append((row[2], row[3]))
    return players

def snake_draft(players, teams):
    assert teams <= 10
    order = list(range(teams))
    reverse_order = list(range(teams))
    reverse_order.reverse()
    order = order + reverse_order
    for i in range(3):
        order = order + order
    team_map_positions = {}
    team_map_no_positions = {}
    for j in range(teams):
        team_map_positions[j] = []
        team_map_no_positions[j] = []

    for team in order:
        my_pick = pick(team_map_positions[team], players)
        team_map_positions[team].append(players[my_pick])
        team_map_no_positions[team].append(players[my_pick][0])
        del players[my_pick]

    return team_map_no_positions

def pick(players, remaining):
    counts = [0, 0, 0, 0]
    for player, position in players:
        counts[POSITIONS_MAP[position]] += 1
    num_players = sum(counts)
    qb_round = max(0, num_players - 4)
    te_round = max(0, num_players - 6)
    qb_factor = (max(0, 2 - counts[0]) ** 4) * (qb_round ** 2)/ 20
    te_factor = (max(0, 2 - counts[3]) ** 4) * (te_round ** 2)/ 20

    qb_found = Infinity
    intervene = False
    for i in range(round(qb_factor)):
        if remaining[i][1] == "QB":
            qb_found = i
            intervene = True
            break
    te_found = Infinity
    for i in range(round(te_factor)):
        if remaining[i][1] == "TE":
            te_found = i
            intervene = True
            break
    if intervene:
        if qb_factor - qb_found >= te_factor - te_found:
            return qb_found
        else:
            return te_found
    else:
        return 0

