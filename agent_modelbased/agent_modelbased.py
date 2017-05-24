import sys

"""
    Team Member
    Name: Mingun Pak            E-mail: mingunpa@usc.edu
    Name: Ali Marjaninejad      E-mail: marjanin@usc.edu
    Name: Qixiong Liu           E-mail: qixiongl@usc.edu
    Name: Chengyu Shen          E-mail: shenchen@usc.edu

    Agent Description
    This is the zombie killer agent. This environment contains two rooms, which are A and B. A is in the left hand side of B.
    If there is a zombie (or more) inside the current room, we need to shoot and kill all the zombie inside this room and move the another then.
    If there is no zombie, we should move to another room.
    model-based: The decision is to make the best estimation based on environment. 
    The only differnece between this and simple reflex agent is when A and B are clean, we do nothing under this situation.
"""

lines = []
intline = []
model = {'A': None, 'B': None}
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())


def modelbased(location, status):
    model[location] = status
    if model['A'] == model['B'] == 'Human':
        return 'NoOp'
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
    action = modelbased(location, status)
    fo.write(action)
    fo.write('\n')
