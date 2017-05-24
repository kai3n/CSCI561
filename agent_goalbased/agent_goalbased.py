import sys

lines = []
intline = []
model = {'A': None, 'B': None}
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())


def goalbased(location, status):
    model[location] = status
    if model['A'] == model['B'] == 'Human':
        return 'Stop'
    elif status == 'Zombie':
        return 'Shoot'
    elif location == 'A':
        return 'Right'
    elif location == 'B':
        return 'Left'


fo = open("output.txt", "wt")
for line in lines:
    splits = line.split(',')
    status = splits[1]
    location = splits[0]
    action = goalbased(location, status)
    if action == 'Stop':
        fo.write(action)
        fo.write('\n')
        break
    fo.write(action)
    fo.write('\n')
