graph = []
with open("testcases/t8.txt", "rt") as fi:
    input_list = [line.rstrip() for line in fi]
print("input_list: {}".format(input_list))
method, fuel, s, d = input_list[0], input_list[1], input_list[2], input_list[3]
print("method: {}".format(method))
print("fuel: {}".format(fuel))
print("s: {}".format(s))
print("d: {}".format(d))
char_dic = {}
index = 0
for node_line in input_list[4:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    target_node = [node_line[0]]
    char_dic[node_line[0]] = index
    index += 1
    for i in range(1, len(node_line)):
        target_node.append(node_line[i].split("-"))
    graph.append(target_node)

print(graph)
print(char_dic)
# def bfs(graph, s, d):
#     queue = [(s, [s], 0)]
#     while queue:
#         (vertex, path, weight) = queue.pop(0)
#         for n, w in graph[char_dic[vertex]][1:]:
#             if n not in set(path):
#                 if int(fuel) >= (weight + int(w)):
#                     if n == d:
#                         return '-'.join(path + [n]) + " " + str(int(fuel) - (weight + int(w)))
#                     else:
#                         queue.append((n, path + [n], weight + int(w)))

def bfs(graph, s, d):
    queue = [(s, [], 0)]
    while queue:
        (vertex, path, weight) = queue.pop(0)
        if vertex not in set(path):
            if int(fuel) >= weight:
                if vertex == d:
                    return '-'.join(path + [vertex]) + " " + str(int(fuel) - weight)
                else:
                    for n, w in graph[char_dic[vertex]][1:]:
                        queue.append((n, path + [vertex], weight + int(w)))
    return "No Path"

def dfs(graph, s, d):
    stack = [(s, [], 0)]
    while stack:
        (vertex, path, weight) = stack.pop()
        if vertex not in set(path):
            if int(fuel) >= weight:
                if vertex == d:
                    return '-'.join(path + [vertex]) + " " + str(int(fuel) - weight)
                else:
                    for n, w in graph[char_dic[vertex]][1:][::-1]:
                        stack.append((n, path + [vertex], weight + int(w)))
    return "No Path"

def ucs(graph, s, d):
    import Queue as Q
    queue = Q.PriorityQueue()
    queue.put((0, s, []))
    while queue:
        (weight, vertex, path) = queue.get()
        if vertex not in set(path):
            if int(fuel) >= weight:
                if vertex == d:
                    return '-'.join(path + [vertex]) + " " + str(int(fuel) - weight)
                else:
                    for n, w in graph[char_dic[vertex]][1:]:
                        queue.put((weight + int(w), n, path + [vertex]))
    return "No Path"

print(ucs(graph, s, d))
# print(dfs(graph, s, d))
