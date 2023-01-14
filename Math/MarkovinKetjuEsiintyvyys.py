import math
import numpy as np

# Laskee  miten usein keskimäärin käydään missäkin tilassa siirtymämatriisin peusteella
# n-1: tilanvaihtojen määrä
# matriisi: Siirtymämatriisi, jokaisen rivin summa oltava 1
# rivi: Millä todennäköisyydellä aloitetaan mistäkin tilasta, summa oltava 1

def pluslasku(a, b):
    valmis = []
    w = len(a)
    for i in range(w):
        temp = []
        for j in range(w):
            q = float(a[i][j])+float(b[i][j])
            temp.append(q)
        valmis.append(temp)
    return valmis


def kertolasku(a,b):
    q = len(a)
    valmis = []
    for i in range(q):
        temp = []
        for j in range(q):
            tot = 0
            for k in range(q):
                tot += float(a[i][k])*float(b[k][j])
            temp.append(tot)
        valmis.append(temp)
    return valmis


def main():


    a = int(input("n-1")) #ts anna suurin potenssi
    b = input("matriisi") #kirjoita kaikki alkiot peräkkäin, erota välilyönnillä
    c = b.split(' ')
    d = math.sqrt(len(c))
    matriisi = []
    for i in range(int(d)):
        temp = []
        for j in range(int(d)):
            temp.append(c[int(d)*i+j])
        matriisi.append(temp)
    e = np.linalg.matrix_power(matriisi, 0)

    q = len(e)
    for i in range(q):
        for j in range(q):
            if e[i][j] == '':
                e[i][j] = 0

    esiintyvyys = e
    for i in range(a):
        temp = list(matriisi)
        power = list(matriisi)
        for j in range(i):
            power = kertolasku(power, temp)
        esiintyvyys = pluslasku(power, esiintyvyys)

    print(esiintyvyys)

    p = input("rivi") #todennäköisyydet millä lähdetään mistäkin ruudusta
    rivi = p.split(' ')
    row = []
    for i in range(q):
        temp = 0
        for j in range(q):
            temp += esiintyvyys[i][j]*float(rivi[j])
        row.append(temp)
    print(row)


main()
