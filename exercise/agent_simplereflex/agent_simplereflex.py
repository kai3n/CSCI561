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
    simple reflex: The decision is totally based on the current situation.

"""

lines = []
intline = []

with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())


def reflex(location, status):
    if status == 'Zombie':
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
    action = reflex(location, status)
    fo.write(action)
    fo.write('\n')
