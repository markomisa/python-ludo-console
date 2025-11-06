import time

p = 10429
q = 10453
m = p * q
seed = int(time.time())
sirina = 8

def bbs():
    global seed
    xn = (seed * seed) % m
    seed = xn
    return xn

def bit_parity(x):
    bit_pom = 0
    while x > 0:
        bit_pom += x % 2
        x //= 2
    return bit_pom % 2

def kocka():
    global sirina
    rnd_broj = 0
    for i in range(sirina):
        rnd_broj *= 2
        rnd_broj += bit_parity(bbs())
    return int((rnd_broj / (2 ** sirina)) * 6 + 1)
