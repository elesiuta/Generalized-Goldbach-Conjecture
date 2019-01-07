# Eric Lesiuta
# Program to generate comets for my generalization of Goldbach's Conjecture

# Changes (2018)
# Rewritten to be slightly more readable than my original version from 2012
# Removed parallelized functions (may rewrite later)

import math
import copy


def factor(n, p):
    """factorization without duplicates.

    Keyword arguments:
    n -- the number for factorization
    p -- the list of possible factors (prime or coprime list)
    """
    n = int(n)
    if 1 in p:
        p = copy.copy(p)
        p.remove(1)
    factors = []
    sqrtn = int(math.sqrt(n)) + 1
    for x in p:
        if n % x == 0:
            factors.append(x)
            n //= x
        while n % x == 0:
            n //= x
        if ((n == 1) | (x > sqrtn)):
            break
    if n != 1:  # if it is prime, or has a prime factor>sqrt(n) (there can only be 1)
        factors.append(n)
    return factors


def primes(stop):
    """returns a list of primes <= stop"""
    primelist = [2, 3, 5]
    tempprimelist = [2]
    tempprimesq = 4
    i = 7
    while i <= stop:
        while tempprimesq < i:
            tempprimelist.append(primelist[len(tempprimelist)])
            tempprimesq = tempprimelist[-1]**2
        prime = True
        for x in tempprimelist:
            if i % x == 0:
                prime = False
                break
        if prime:
            primelist.append(i)
        i += 2
    return primelist


def coprimelist(n, primes):
    """returns the minimal list of coprimes where each element modulo n = 1
    any number that is a multiple of n and > n**2 can be written as the sum of n items from this list
    optimized to run quickly for generating longer lists (if you provide your own primes since the above one isn't too efficient)
    """
    primes = copy.copy(primes)
    maxprime = primes[-1]

    # eg for goldbach's conjecture, this bit of code will remove 2, which only affects 4 = 2 + 2
    # according to my rules though, each number must have a %n == 1 therefore these numbers or any multiples can't be used
    for x in factor(n, primes):
        if x in primes:
            primes.remove(x)

    coprimes = []
    remainingPrimeFactors = []
    for x in primes:
        if x % n == 1:
            coprimes.append(x)
        else:
            remainingPrimeFactors.append(x)
    for x in range(n+1, maxprime, n):
        isCoprime = True
        for f in factor(x, primes):
            if f not in remainingPrimeFactors:
                isCoprime = False
        if isCoprime:
            coprimes.append(x)
            for f in factor(x, primes):
                remainingPrimeFactors.remove(f)
    return coprimes


def gcd(a, b):
    """returns the greatest common divisor using Euclid's algorithm"""
    if a == 0 or b == 0:
        return 0
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    if a == 0:
        return b
    else:
        return a


def simplecoprimelist(n, stop):
    """simplified, but slower version of the function coprimelist"""
    coprimes = [n+1]
    for i in range(n+1, stop, n):
        coprime = True
        for c in coprimes:
            if gcd(i, c) != 1:
                coprime = False
        if coprime:
            coprimes.append(i)
    return coprimes


def createcomet(n, stop):
    """generates a comet for a generalization with base n, for all numbers up to stop
    the output comet[i] is the number of ways n*i can be represented as a sum of n coprimes from coprimelist
    """

    # these variable names make more sense in the previous, recursive version of this function
    cd = 1  # current array depth
    md = int(n)  # max depth = n
    sums = [0]*(n+1)  # sums (at each depth)
    index = [0]*(n+1)  # index (at each depth)
    coprimes = coprimelist(n, primes(stop))
    lencp = len(coprimes)
    comet = [0]*(stop)

    while(True):
        sums[cd] = sums[cd-1] + coprimes[index[cd]]
        index[cd] += 1
        cd += 1
        if cd == md:
            for x in range(index[-2]-1, lencp):
                y = (sums[-2] + coprimes[x])//md
                comet[y] += 1
            cd -= 1
            while(index[cd] == lencp):
                cd -= 1
            for x in range(cd, md):
                index[x+1] = index[x]
            if (cd == 0):
                break

    return comet[:stop//n+1]


def writecomet(n, comet):
    """writes the comet/distribution with each entry on a new line"""
    f = open("n="+str(n)+".txt", "w")
    for x in comet:
        f.write(str(x)+"\n")
    f.close()


def plotcomet(n, stop, comet):
    """plots the comet/distribution, the number of ways 'x' can be written as a sum of 'n' coprimes from the set generated with coprimelist"""
    import matplotlib.pyplot as plt
    X = [x for x in range(0, stop+1, n)]
    Y = comet[:len(X)]
    plt.figure(figsize=(15, 15))
    plt.scatter(X, Y, s=1)
    plt.grid(True)
    plt.savefig("n="+str(n)+".png", format="png", dpi=400)
    plt.clf()


def writeandplot(n, stop):
    """generates, writes and plots the distribution"""
    comet = createcomet(n, stop)
    writecomet(n, comet)
    plotcomet(n, stop, comet)
