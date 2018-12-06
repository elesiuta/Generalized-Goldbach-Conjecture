# Eric Lesiuta
# Version from Tue, May 1, 2012 at 1:36 AM

import itertools
import collections

def pf (n):
    ##prime factorization (modified to get rid of duplicates)
    from math import sqrt
    n = int(n)
    factors = []
    if n%2 == 0:
        n//=2
        factors.append(2)
    while n%2 == 0:
        n//=2
    for x in range (3,int(sqrt(n))+1,2):
        if n%x == 0:
            factors.append(x)
            n //= x
        while n%x == 0:
            n //= x
            if n == 1:
                break
    if n != 1: ##if it is prime, or has a prime factor>sqrt(n) (there can only be 1)
        factors.append(n)
    return factors

def primes(e):
    primelist = [1, 2, 3, 5]
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

def checksum(e, n, s):
    ##check if e can be written as the sum of n numbers from set s
    ##VERY INEFFICENT
    for x in set(itertools.combinations_with_replacement(s,n)):
        if (sum(x) == e):
            return x
    return False

def bettersum(n, s):
    ##creates lis of e that can be written as the sum of n numbers from set s
    output = []
    for x in set(itertools.combinations_with_replacement(s,n)):
        output.append(sum(x))
    return list(sorted(collections.Counter(output)))

def maxsum(n, l):
    ##finds the real max number from bettersum (since there are some stragglers higher up)
    for i in range(0,len(l)):
        if (l[i] != n * (i+1)):
            return n*i
    return l[-1]

def makelist(n,primes):
    ##BUG ON n = 7, should choose 2^3 over 2*11, keep code just in case, I like what I did and may use somewhere else
    ##makes the set of coprimes that can be used to sum to any number multiple of n, requires list of primes (size depends on how much to test)
    maxprime = primes[-1]
    for x in pf(n):
        if (primes.count(x)==1):
            primes.remove(x)
    coprimes = []
    temp = []
    for x in primes:
        if x%n == 1:
            coprimes.append(x)
        else:
            temp.append(x)
    while temp != []:
        ln = temp
        lp = [0]*len(temp)
        lp[0] = 2
        while(resolve(ln,lp)%n != 1):
            try:
                ##I think I fixed it, should work
                if (ln[0]**lp[0] < ln[1]):
                    lp[0] += 1
                elif(ln[0]**lp[0] > ln[1]):
                    lp[0] = 1
                    lp[1] += 1
                    ##like counting in a number system where each place is a different base (LS# != 0, maybe not?) (this was my flaw in logic for n=7)
                    for x in range(1,len(lp)-1):
                        if((ln[x]**lp[x] > ln[x+1])):
                            lp[x] = 0
                            lp[x+1] += 1
            except:
                lp[0] += 1
        ##little bit of cleanup, no point working with sparse numbers about what we're testing
        coprimes.append(resolve(ln,lp))
        if (coprimes[-1] > maxprime):
            return coprimes[0:-1]
        temp = clean(ln,lp)
    return coprimes

def resolve(ln,lp):
    ##list of numbers, list of powers
    ##eg. ln = [2,3,5,7], lp = [2,1,0,0], is 2^2*3^1*5^0*7^0
    ##used by makelist
    x = 1
    for i in range(0,len(ln)):
        x *= ln[i]**lp[i]
    return x

def clean(ln,lp):
    ##used by makelist
    ##takes out any primes that are used so all the numbers in the final list are coprime
    lc = []+ln
    for i in range(0,len(ln)):
        if lp[i] != 0:
            lc.remove(ln[i])
    return lc

def betterlist(n, primes):
    ##makes the set of coprimes that can be used to sum to any number multiple of n, requires list of primes (size depends on how much to test)
    maxprime = primes[-1]
    for x in pf(n):
        if (primes.count(x)==1):
            primes.remove(x)
    coprimes = []
    temp = []
    for x in primes:
        if x%n == 1:
            coprimes.append(x)
        else:
            temp.append(x)
    for x in range(n+1,maxprime,n):
        has = True
        for y in pf(x):
            if temp.count(y) == 0:
                has = False
        if has == True:
            coprimes.append(x)
            for y in pf(x):
                temp.remove(y)
    return coprimes

def quicktest(n,upper):
    s = betterlist(n,primes(upper))
    a = bettersum(n,s)
    return maxsum(n,a)