graph = []
with open("testcases/t1.txt", "rt") as fi:
    input_list = [line.rstrip() for line in fi]
print("input_list: {}".format(input_list))
method, fuel, s, d = input_list[0], input_list[1], input_list[2], input_list[3]
print("method: {}".format(method))
print("fuel: {}".format(fuel))
print("s: {}".format(s))
print("d: {}".format(d))
for node_line in input_list[4:]:
    node_line = node_line.replace(":", "").replace(",", "").split()
    target_node = [node_line[0]]
    for i in range(1, len(node_line)):
        target_node.append(node_line[i].split("-"))
    graph.append(target_node)

print(graph)
