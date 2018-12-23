# Eric Lesiuta
# Program to generate comets for my generalization of Goldbach's Conjecture

# Changes (2018)
# Rewritten to be slightly more readable than my original version from 2012
# Removed parallelized functions (may rewrite later)

import math
import copy

def factor(n,p):
    """factorization without duplicates.

    Keyword arguments:
    n -- the number for factorization
    p -- the list of possible factors (prime or coprime list)
    """
    n = int(n)
    if p.count(1) == 1:
        p = copy.copy(p)
        p.remove(1)
    factors = []
    sqrtn = int(math.sqrt(n)) + 1
    for x in p:
        if n%x == 0:
            factors.append(x)
            n //= x
        while n%x == 0:
            n //= x
        if ((n == 1) | (x > sqrtn)):
            break
    if n != 1: ##if it is prime, or has a prime factor>sqrt(n) (there can only be 1)
        factors.append(n)
    return factors

def primes(e):
    """returns a list of primes <= e"""
    primelist = [2, 3, 5]
    tempprimelist = [2]
    tempprimesq = 4
    s = 7
    while s<=e:
        while tempprimesq < s:
            tempprimelist.append(primelist[len(tempprimelist)])
            tempprimesq = tempprimelist[-1]**2
        prime = True
        for x in tempprimelist:
            if s%x==0:
                prime = False
                break
        if prime == True:
            primelist.append(s)
        s+=2
    return primelist

def coprimelist(n, primes):
    """returns the set of coprimes that can be used to sum to any number that is a multiple of n and > n**2"""
    primes = copy.copy(primes)
    maxprime = primes[-1]

    # eg for goldbach's conjecture, this bit of code will remove 2, which only affects 4 = 2 + 2
    # according to my rules though, each number must have a %n == 1 therefore these numbers or any multiples can't be used
    for x in factor(n,primes):
        if (primes.count(x)==1):
            primes.remove(x)

    coprimes = []
    remainingPrimeFactors = []
    for x in primes:
        if x%n == 1:
            coprimes.append(x)
        else:
            remainingPrimeFactors.append(x)
    for x in range(n+1,maxprime,n):
        isCoprime = True
        for f in factor(x,primes):
            if f not in remainingPrimeFactors:
                isCoprime = False
        if isCoprime:
            coprimes.append(x)
            for f in factor(x,primes):
                remainingPrimeFactors.remove(f)
    return coprimes

def createcomet(n,limit):
    """generates a comet for a generalization with base n, for all numbers up to limit
    the output comet[i] is the number of ways n*i can be represented as a sum of n coprimes from coprimelist
    """
    
    # these variable names make more sense in the previous, recursive version of this function
    cd = 1 ##current array depth
    md = int(n) ##max depth = n
    sums = [0]*(n+1) ##sums (at each depth)
    index = [0]*(n+1) ##index (at each depth)
    coprimes = coprimelist(n,primes(limit))
    lencp = len(coprimes)
    comet = [0]*(limit)

    while(True):
        sums[cd] = sums[cd-1] + coprimes[index[cd]]
        index[cd] += 1
        cd += 1
        if cd == md:
            for x in range(index[-2]-1,lencp):
                y = (sums[-2] + coprimes[x])//md
                comet[y] += 1
            cd -= 1
            while(index[cd] == lencp):
                cd -= 1
            for x in range(cd, md):
                index[x+1] = index[x]
            if (cd == 0):
                break

    return comet[:limit//n+1]

def writecomet(n,comet):
    """writes the comet/distribution with each entry on a new line"""
    f = open(str(n)+"_GB2018.txt","w")
    for x in comet:
        f.write(str(x)+"\n")
    f.close()

def plotcomet(n,limit,comet):
    """plots the comet/distribution, the number of ways 'x' can be written as a sum of 'n' coprimes from the set generated with coprimelist"""
    import matplotlib.pyplot as plt
    X = [x for x in range(0,limit+1,n)]
    Y = comet[:len(X)]
    plt.figure(figsize=(15, 15))
    plt.scatter(X,Y,s=1)
    plt.grid(True)
    plt.savefig(str(n)+"_GB2018.png", format="png", dpi=400)
    plt.clf()

def writeandplot(n,limit):
    """generates, writes and plots the distribution"""
    comet = createcomet(n,limit)
    writecomet(n,comet)
    plotcomet(n,limit,comet)
