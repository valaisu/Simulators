import math

#Calculates the otrhonormal base of a vector.
#Give input in format (x,y,z,...) [enter] . [enter]

def sisT(x,y):
    tot = 0
    print(x)
    print(y)
    for i in range(len(x)):
        tot += x(i)*y
    return tot

def pituus(x):
    tot = 0
    for i in range(len(x)):
        tot += int(x[i])*int(x[i])
    return math.sqrt(tot)

def main():
    vectors = []
    a = ""
    while a != ".":
        a = input("Syötä vektori muodossa x,y,z... tai lopeta pisteellä(.)")
        aSplit = a.split(",")
        vectors.append(aSplit)
    del vectors[len(vectors)-1]
    print(vectors)
    newVecs = []
    ekaPituus = pituus(vectors[0])
    tempVec = []
    for i in range(len(vectors[0])):
        tempVec.append(float(vectors[0][i])/ekaPituus)
    newVecs.append(tempVec)

    for i in range(len(vectors)-1):
        tempList = []
        for j in range(i+1):
            a = sisT(vectors[len(vectors)-1], newVecs[j])

            b = newVecs[j]
            c = []
            for k in range(len(b)):
                c.append(b[k]*a)
            tempList.append(c)
        negVec = vectors[i+1]
        for l in range(len(tempList)):
            negVec[0] += tempList[l][0]
            negVec[1] += tempList[l][1]
            negVec[2] += tempList[l][2]
        newVecs.append(negVec)
    print(newVecs)
main()
