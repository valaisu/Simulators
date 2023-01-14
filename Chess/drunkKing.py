import random

# In a game of chess, imagine a lonely king on the board.
# Assuming king moves randomly, this program calculates how
# often (roughly) the king finds itself on different kind of
# squares.

def move(x):
    cons = []
    t = [int(x[0]),int(x[1])]
    for i in range(3):
        for j in range(3):
            temp = str(t[0]-1+i)+str(t[1]-1+j)
            if 0<int(temp[0])<6 and 0<int(temp[1])<6:
                cons.append(temp)
    q = len(cons)
    a = random.randint(0, (q-1))
    return cons[a]


def main():
    a = "12345"
    n = "12345"
    m = []
    for i in range(len(a)):
        temp = []
        for j in range(len(a)):
            t = str(a[i])+str(n[j])
            temp.append(t)
        m.append(temp)
    print(m)
    start = "11"

    center = 0
    centrish = 0
    edge = 0
    corner = 0

    b = move(start)
    location = b
    for i in range(1000000):
        b = move(location)
        location = b
        if b == "33":
            center += 1
        if b == "22":
            centrish += 1
        if b == "11":
            corner += 1
        if b == "21":
            edge += 1
    print(center)
    print(centrish)
    print(edge)
    print(corner)

main()
