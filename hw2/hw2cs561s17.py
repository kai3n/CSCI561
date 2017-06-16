from copy import deepcopy
import time

with open('testcases/t5.txt', 'rt') as fi:
    input_list = [line.rstrip() for line in fi]

colors = input_list[0].replace(' ', '').split(',')
print colors

initial_map_color = list()
for i in input_list[1].replace(' ', '').split(','):
    m = i.split(':')[0]
    c = i.split(':')[1].split('-')[0]
    p = i.split(':')[1].split('-')[1]
    initial_map_color.append([m, c, p])

print initial_map_color

maximum_depth = int(input_list[2])
print maximum_depth

preferences_of_player1 = dict()
preferences_of_player2 = dict()

for i in input_list[3].replace(' ', '').split(','):
    preferences_of_player1[i.split(':')[0]] = i.split(':')[1]
for i in input_list[4].replace(' ', '').split(','):
    preferences_of_player2[i.split(':')[0]] = i.split(':')[1]

print preferences_of_player1
print preferences_of_player2

# build a graph.
char_dic = {}
node_list = []
graph = [[False for _ in range(len(input_list)-5)] for _ in range(len(input_list)-5)]
index = 0
for node_line in input_list[5:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    char_dic[node_line[0]] = index
    node_list.append(node_line[0])
    index += 1
print(char_dic)
print node_list
for node_line in input_list[5:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    print(node_line)
    for i in node_line[1:]:
        graph[char_dic[node_line[0]]][char_dic[i]] = True
        graph[char_dic[i]][char_dic[node_line[0]]] = True

def init_map(graph, initial_map_color):
    for i in initial_map_color:
        graph[char_dic[i[0]]][char_dic[i[0]]] = [i[1], i[2]]
    return graph

graph = init_map(graph, initial_map_color)
print graph
print "========================build success========================"

def isTerminal(state):
    for i in range(len(char_dic)):
        constrained_color = set()
        if not state[i][i]:  # uncolored area
            for j in range(len(char_dic)):
                if j == i:
                    continue
                if state[i][j] and (type(state[j][j]) == type(list())):  # adjacent area
                    constrained_color.add(state[j][j][0])
            if len(set(colors) - constrained_color) != 0:
                return False
    return True

def utility(state):
    score_of_player1 = 0
    score_of_player2 = 0

    for i in range(len(char_dic)):
        if state[i][i]:
            if state[i][i][1] == '1':  # player1
                score_of_player1 += int(preferences_of_player1.get(state[i][i][0]))
            else:  # player2
                score_of_player2 += int(preferences_of_player2.get(state[i][i][0]))
    #print'score_of_player1-score_of_player2:',(score_of_player1-score_of_player2)
    # print state
    return score_of_player1-score_of_player2

def make_child(state, player):
    states = list()
    for i in range(len(char_dic)):
        constrained_color = set()
        if not state[i][i]:  # uncolored area
            for j in range(len(char_dic)):
                if state[i][j]:  # adjacent areas
                    if state[j][j]:  # colored area
                        constrained_color.add(state[j][j][0])
            for color in set(colors) - constrained_color:  # TODO: consider the order again
                tmp_state = deepcopy(state)
                tmp_state[i][i] = [color, player]
                # print tmp_state
                states.append(tmp_state)
    # print len(states)
    return states

def minimax(state, depth, alpha, beta, maximizingPlayer):
    if depth == maximum_depth:# or isTerminal(state):
        return utility(state)

    if maximizingPlayer:
        best_value = float('-inf')
        for child in make_child(state, '1'):

            print depth, best_value, alpha, beta  # add node visit log here

            v = minimax(child, depth+1, alpha, beta, False)
            if best_value < v:
                best_value = v
                print depth, best_value, alpha, beta  # update log
            if best_value >= beta:
                return best_value
            alpha = max(alpha, best_value)

        #print "max value", best_value
        return best_value
    else:
        best_value = float('inf')
        for child in make_child(state, '2'):

            print depth, best_value, alpha, beta  # add node visit log here

            v = minimax(child, depth+1, alpha, beta, True)
            if best_value > v:
                best_value = v
                print depth, best_value, alpha, beta  # update log
            if best_value <= alpha:
                return best_value
            beta = min(beta, best_value)
        # print "min value", best_value
        return best_value

alpha = float('-inf')
beta = float('inf')
print(minimax(graph, 0, alpha, beta, True))
