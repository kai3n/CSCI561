from copy import deepcopy
import time

with open('testcases/t6.txt', 'rt') as fi:
    input_list = [line.rstrip() for line in fi]

colors = input_list[0].replace(' ', '').split(',')
colors = sorted(colors)
print 'colors: ', colors

initial_map_color = list()
for i in input_list[1].replace(' ', '').split(','):
    m = i.split(':')[0]
    c = i.split(':')[1].split('-')[0]
    p = i.split(':')[1].split('-')[1]
    initial_map_color.append([m, c, p])

print 'initial_map_color: ', initial_map_color

maximum_depth = int(input_list[2])
print 'maximum_depth: ', maximum_depth

preferences_of_player1 = dict()
preferences_of_player2 = dict()

for i in input_list[3].replace(' ', '').split(','):
    preferences_of_player1[i.split(':')[0]] = i.split(':')[1]
for i in input_list[4].replace(' ', '').split(','):
    preferences_of_player2[i.split(':')[0]] = i.split(':')[1]

print 'preferences_of_player1: ', preferences_of_player1
print 'preferences_of_player2: ', preferences_of_player2

# build a graph.
char_dic = {}
node_list = []
graph = [[False for _ in xrange(len(input_list)-5)] for _ in xrange(len(input_list)-5)]
index = 0
for node_line in input_list[5:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    node_list.append(node_line[0])

node_list = sorted(node_list)
for i in xrange(len(node_list)):
    char_dic[node_list[i]] = i
print 'node_list: ', node_list
print 'char_dic: ', char_dic

for node_line in input_list[5:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    for i in node_line[1:]:
        graph[char_dic[node_line[0]]][char_dic[i]] = True
        graph[char_dic[i]][char_dic[node_line[0]]] = True

def init_map(graph, initial_map_color):
    for i in initial_map_color:
        graph[char_dic[i[0]]][char_dic[i[0]]] = [i[1], i[2]]
    return graph

graph = init_map(graph, initial_map_color)
print 'initial graph: ', graph
print "========================build success========================"

logs = []

def isTerminal(state):
    for i in xrange(len(char_dic)):
        constrained_color = set()
        if not state[i][i]:  # uncolored area
            for j in xrange(len(char_dic)):
                if j == i:
                    continue
                if state[i][j] and (type(state[j][j]) == type(list())):  # adjacent area
                    constrained_color.add(state[j][j][0])
            if len(set(colors) - constrained_color) != 0:
                return False
    return True

def utility(state, current_node, current_color, depth, value, alpha, beta):
    score_of_player1 = 0
    score_of_player2 = 0

    for i in xrange(len(char_dic)):
        if state[i][i]:
            if state[i][i][1] == '1':  # player1
                score_of_player1 += int(preferences_of_player1.get(state[i][i][0]))
            else:  # player2
                score_of_player2 += int(preferences_of_player2.get(state[i][i][0]))
    logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(score_of_player1-score_of_player2) + ', ' + str(alpha) + ', ' + str(
        beta))
    return score_of_player1-score_of_player2

def make_child(state, player):
    states = list()
    for i in xrange(len(char_dic)):
        constrained_color = list()
        if not state[i][i]:  # uncolored area
            for j in xrange(len(char_dic)):
                if state[i][j]:  # adjacent areas
                    if state[j][j]:  # colored area
                        constrained_color.append(state[j][j][0])
            if (len(set(constrained_color)) == len(colors)) or len(constrained_color) == 0:
                continue
            for color in colors:
                if color not in constrained_color:
                    tmp_state = deepcopy(state)
                    tmp_state[i][i] = [color, player]
                    # print tmp_state
                    states.append((tmp_state, [node_list[i], color]))
    # print len(states)
    return states

action_node = []
def minimax(state, current_node, current_color, depth, value, alpha, beta, maximizingPlayer):
    global action_node
    if depth == maximum_depth or isTerminal(state):
        return utility(state, current_node, current_color, depth, value, alpha, beta)

    if maximizingPlayer:
        best_value = float('-inf')
        logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
            alpha) + ', ' + str(beta))
        for child_state, child_node in make_child(state, '1'):

            v = minimax(child_state, child_node[0], child_node[1], depth+1, beta, alpha, beta, False)
            if best_value < v:
                best_value = v
                if depth == 0:
                    action_node = child_node

            if best_value >= beta:
                logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                    alpha) + ', ' + str(beta))  # update log
                return best_value
            alpha = max(alpha, best_value)
            logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                alpha) + ', ' + str(beta)) # update log

        return best_value
    else:
        best_value = float('inf')
        logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
            alpha) + ', ' + str(beta))
        for child_state, child_node in make_child(state, '2'):

            v = minimax(child_state, child_node[0], child_node[1], depth+1, alpha, alpha, beta, True)
            if best_value > v:
                best_value = v
            if best_value <= alpha:
                logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                    alpha) + ', ' + str(beta))  # update log
                return best_value
            beta = min(beta, best_value)
            logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
            alpha) + ', ' + str(beta))  # update log

        return best_value

alpha = float('-inf')
beta = float('inf')
value = float('-inf')
import time
start = time.time()
utility = minimax(graph, initial_map_color[-1][0], initial_map_color[-1][1], 0, value, alpha, beta, True)
best_node_of_first_move = action_node[0]
best_color_of_first_move = action_node[1]
logs.append(best_node_of_first_move + ', ' + best_color_of_first_move + ', ' + str(utility))

content = ""
for log in logs:
    content += log + '\n'
content = content[:-1]

print(content)
with open('testcases/output_t6.txt', 'rt') as fi:
    output = fi.read()

if output == content:
    print('Good Job!')
else:
    print('Sorry!')

finish = time.time() - start
print(finish)
