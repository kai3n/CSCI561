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
    Goal-based: Goal describes what agent wants. Our goal for this task is make both rooms are clean. So if both of them are clean, we terminate the program.

"""
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
