import fileinput

ind = 0
for line in fileinput.input():
    ind = line.find("(CNN)")
    if ind != -1:
        line = line[ind+5:]
    print(line)