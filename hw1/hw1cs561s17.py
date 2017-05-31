import sys
import Queue as Q

char_dic = {}


class DeliveryDrone(object):
    def __init__(self, graph, fuel):
        self.graph = graph
        self.fuel = fuel

    def bfs(self, s, d):
        queue = [(s, [], 0)]
        while queue:
            (vertex, path, weight) = queue.pop(0)
            if vertex not in set(path):
                if int(self.fuel) >= weight:
                    if vertex == d:
                        return '-'.join(path + [vertex]) + " " + str(int(self.fuel) - weight)
                    else:
                        for n, w in self.graph[char_dic[vertex]][1:]:
                            queue.append((n, path + [vertex], weight + int(w)))
        return "No Path"

    def dfs(self, s, d):
        stack = [(s, [], 0)]
        while stack:
            (vertex, path, weight) = stack.pop()
            if vertex not in set(path):
                if int(self.fuel) >= weight:
                    if vertex == d:
                        return '-'.join(path + [vertex]) + " " + str(int(self.fuel) - weight)
                    else:
                        for n, w in self.graph[char_dic[vertex]][1:][::-1]:
                            stack.append((n, path + [vertex], weight + int(w)))
        return "No Path"

    def ucs(self, s, d):
        queue = Q.PriorityQueue()
        queue.put((0, s, []))
        while queue:
            (weight, vertex, path) = queue.get()
            if vertex not in set(path):
                if int(self.fuel) >= weight:
                    if vertex == d:
                        return '-'.join(path + [vertex]) + " " + str(int(self.fuel) - weight)
                    else:
                        for n, w in self.graph[char_dic[vertex]][1:]:
                            queue.put((weight + int(w), n, path + [vertex]))
        return "No Path"


def main():
    graph = []
    path = ""

    with open(sys.argv[2], "rt") as fi:
        input_list = [line.rstrip() for line in fi]

    method, fuel, s, d = input_list[0], input_list[1], input_list[2], input_list[3]

    # build a graph.
    index = 0
    for node_line in input_list[4:]:
        node_line = node_line.replace(":", "").replace(",", "").split()
        target_node = [node_line[0]]
        char_dic[node_line[0]] = index
        index += 1
        for i in range(1, len(node_line)):
            target_node.append(node_line[i].split("-"))
        graph.append(target_node)

    # select search method.
    drone = DeliveryDrone(graph, fuel)
    if method == "BFS":
        path = drone.bfs(s, d)
    elif method == "DFS":
        path = drone.dfs(s, d)
    elif method == "UCS":
        path = drone.ucs(s, d)
    else:
        path = "No Path"

    with open("output.txt", "wt") as fo:
        fo.writelines(path)

if __name__ == "__main__":
    main()