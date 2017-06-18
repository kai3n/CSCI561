import sys
import time


class GameTreeSearch(object):

    def __init__(self, node_len, colors, preferences_of_player1, preferences_of_player2, node_list, maximum_depth):
        self.node_len = node_len
        self.colors = colors
        self.preferences_of_player1 = preferences_of_player1
        self.preferences_of_player2 = preferences_of_player2
        self.node_list = node_list
        self.maximum_depth = maximum_depth
        self.logs = []
        self.action_node = []
        self.action_color = ''

    def isTerminal(self, state):
        for i in xrange(self.node_len):
            constrained_color = set()
            if not state[i][i]:  # uncolored area
                for j in xrange(self.node_len):
                    if j == i:
                        continue
                    if state[i][j] and (type(state[j][j]) == type(list())):  # adjacent area
                        constrained_color.add(state[j][j][0])
                if len(set(self.colors) - constrained_color) != 0:
                    return False
        return True

    def utility(self, state, current_node, current_color, depth, alpha, beta):
        score_of_player1 = 0
        score_of_player2 = 0

        for i in xrange(self.node_len):
            if state[i][i]:
                if state[i][i][1] == '1':  # player1
                    score_of_player1 += int(self.preferences_of_player1.get(state[i][i][0]))
                else:  # player2
                    score_of_player2 += int(self.preferences_of_player2.get(state[i][i][0]))
        self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(score_of_player1-score_of_player2) + ', ' + str(alpha) + ', ' + str(
            beta))
        return score_of_player1-score_of_player2

    def make_child(self, state):
        actions = list()
        for i in list(xrange(self.node_len)):
            constrained_color = set()
            if not state[i][i]:  # uncolored area
                for j in list(xrange(self.node_len)):
                    if state[i][j]:  # adjacent areas
                        if state[j][j]:  # colored area
                            constrained_color.add(state[j][j][0])
                if (len(constrained_color) == len(self.colors)) or len(constrained_color) == 0:
                    continue
                for color in self.colors:
                    if color not in constrained_color:
                        actions.append([i, color])
        return actions

    def minimax(self, state, current_node, current_color, depth, alpha, beta, maximizingPlayer):
        if depth == self.maximum_depth or self.isTerminal(state):
            return self.utility(state, current_node, current_color, depth, alpha, beta)

        if maximizingPlayer:
            best_value = float('-inf')
            self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                alpha) + ', ' + str(beta))
            for a_node, a_color in self.make_child(state):

                state[a_node][a_node] = [a_color, '1']
                v = self.minimax(state, self.node_list[a_node], a_color, depth+1, alpha, beta, False)
                state[a_node][a_node] = False

                if best_value < v:
                    best_value = v
                    if depth == 0:
                        self.action_node = self.node_list[a_node]
                        self.action_color = a_color

                if best_value >= beta:
                    self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                        alpha) + ', ' + str(beta))
                    return best_value
                alpha = max(alpha, best_value)
                self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                    alpha) + ', ' + str(beta))

            return best_value
        else:
            best_value = float('inf')
            self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                alpha) + ', ' + str(beta))
            for a_node, a_color in self.make_child(state):

                state[a_node][a_node] = [a_color, '2']
                v = self.minimax(state, self.node_list[a_node], a_color, depth + 1, alpha, beta, True)
                state[a_node][a_node] = False
                if best_value > v:
                    best_value = v
                if best_value <= alpha:
                    self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                        alpha) + ', ' + str(beta))
                    return best_value
                beta = min(beta, best_value)
                self.logs.append(current_node + ', ' + current_color + ', ' + str(depth) + ', ' + str(best_value) + ', ' + str(
                alpha) + ', ' + str(beta))

            return best_value

def main():
    with open(sys.argv[2], 'rt') as fi:
        input_list = [line.rstrip() for line in fi]

    colors = input_list[0].replace(' ', '').split(',')
    colors = sorted(colors)

    initial_map_color = list()
    for i in input_list[1].replace(' ', '').split(','):
        m = i.split(':')[0]
        c = i.split(':')[1].split('-')[0]
        p = i.split(':')[1].split('-')[1]
        initial_map_color.append([m, c, p])

    maximum_depth = int(input_list[2])

    preferences_of_player1 = dict()
    preferences_of_player2 = dict()

    for i in input_list[3].replace(' ', '').split(','):
        preferences_of_player1[i.split(':')[0]] = i.split(':')[1]
    for i in input_list[4].replace(' ', '').split(','):
        preferences_of_player2[i.split(':')[0]] = i.split(':')[1]

    # build a graph.
    char_dic = {}
    node_list = []
    graph = [[False for _ in xrange(len(input_list) - 5)] for _ in xrange(len(input_list) - 5)]

    for node_line in input_list[5:]:
        node_line = node_line.replace(":", "").replace(",", "").split()
        node_list.append(node_line[0])

    node_list = sorted(node_list)
    for i in xrange(len(node_list)):
        char_dic[node_list[i]] = i

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
    node_len = len(char_dic)
    alpha = float('-inf')
    beta = float('inf')

    csp = GameTreeSearch(node_len, colors, preferences_of_player1, preferences_of_player2, node_list, maximum_depth)
    utility = csp.minimax(graph, initial_map_color[-1][0], initial_map_color[-1][1], 0, alpha, beta, True)
    best_node_of_first_move = csp.action_node
    best_color_of_first_move = csp.action_color
    csp.logs.append(best_node_of_first_move + ', ' + best_color_of_first_move + ', ' + str(utility))

    content = ""
    for log in csp.logs:
        content += log + '\n'
    content = content[:-1]

    with open('output.txt', 'wt') as fo:
        fo.write(content)

    # if output == content:
    #     print('Good Job!')
    # else:
    #     print('Sorry!')
    #

if __name__ == '__main__':
    main()
    """
    Question1: Is there any cases that has no initial map coloring?
    """