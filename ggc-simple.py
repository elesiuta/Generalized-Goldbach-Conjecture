import itertools
import collections
import sys
from multiprocessing import Pool, cpu_count, Queue, queues, Manager
import timeit
import time
import ctypes
import copy
##Python does not seem to follow any rules like c/java when it comes to passing
##by reference or value, so I'll just use copy!

##default is 1000
sys.setrecursionlimit(100000)

##Returns a list of prime factors for number n, requires a list of primes p
def pf (n,p):
    ##prime factorization (modified to get rid of duplicates)
    from math import sqrt
    n = int(n)
    factors = []
    if n%2 == 0:
        n//=2
        factors.append(2)
    while n%2 == 0:
        n//=2
    sqrtn = int(sqrt(n)) + 1
    for x in p[2:]:
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

##Returns a list of prime number up to e
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
    
"""
Returns a list of every prime number where primeNumber%n=1 and the smallest numbers that are coprime with all other numbers in the set where coprime%n=1
"""
def betterlist(n, primes):
    ##makes the set of coprimes that can be used to sum to any number multiple of n, requires list of primes (size depends on how much to test)
    maxprime = primes[-1]
    p = copy.copy(primes)
    for x in pf(n,p):
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
        for y in pf(x,p):
            if temp.count(y) == 0:
                has = False
        if has == True:
            coprimes.append(x)
            for y in pf(x,p):
                temp.remove(y)
    return coprimes

"""
Functions that check which numbers can be written as a sum from my list
"""
##depreciated
def checksum(e, n, s):
    ##check if e can be written as the sum of n numbers from set s
    ##VERY INEFFICENT
    for x in set(itertools.combinations_with_replacement(s,n)):
        if (sum(x) == e):
            return x
    return False

##depreciated
def bettersum(n, s):
    ##creates lis of e that can be written as the sum of n numbers from set s
    output = []
    for x in set(itertools.combinations_with_replacement(s,n)):
        output.append(sum(x))
    return list(sorted(collections.Counter(output)))

##depreciated
def maxsum(n, l):
    ##finds the real max number from bettersum (since there are some stragglers higher up)
    for i in range(0,len(l)):
        if (l[i] != n * (i+1)):
            return n*i
    return l[-1]

##depreciated
def fastersum(n, s, upper):
    ##creates lis of e that can be written as the sum of n numbers from set s
    ##stores it a bit differently(hash) for efficiency, has upper limit, need to choose one big enough
    output = [0]*upper
    start = timeit.time.time()
    for x in set(itertools.combinations_with_replacement(s,n)):
        try:
            output[int(sum(x)/n)] += 1
        except:
            pass
    print (timeit.time.time() - start)
    for i in range(1,len(output)):
        if output[i] == 0:
            return (i-1)*n
    return (i*n)

##just bad
##Costs lots of ram, isn't that fast either
def sumn(x):
    return (int(sum(x)/len(x)))
def mfastersum(n, s, upper):
    ##creates lis of e that can be written as the sum of n numbers from set s
    ##stores it a bit differently(hash) for efficiency, has upper limit, need to choose one big enough
    output = [0]*upper
    start = timeit.time.time()
    pool = Pool(PROCESSES)
    for x in pool.map(sumn,itertools.combinations_with_replacement(s,n),1000):
        try:
            output[x] += 1
        except:
            pass
    print (timeit.time.time() - start)
    return output
    for i in range(1,len(output)):
        if output[i] == 0:
            return (i-1)*n
    return (i*n)

##SINGLE PROCESS
##AHHHHHH THIS LOOKS DISGUSTING BUT I DONT KNOW HOW ELSE TO DO THIS
##currently the best version
global globlist

def combinations(cd, md, sum, i, l):
    ##returns sum of combinations
    ##current depth, max depth, sum, index, list
    global globlist
    for x in range(i, len(l)):
        if cd < md:
            combinations(cd+1,md,sum+l[x],x,l)
        else:
            try:
                globlist[int((sum+l[x])/md)] += 1
            except:
                pass

def smallersum(n, s, upper, q):
    ##creates lis of e that can be written as the sum of n numbers from set s
    ##uses my own function for combinations so they don't all stay stored in memory
    global globlist
    globlist = [0]*upper
    for x in range(0,len(s)):
        combinations(2,n,s[x],x,s)
        ##debug info, uses q
        if(x%10 == 0):
            q.put("For n:"+str(n)+" Progress:"+str(x)+"/"+str(len(s))+" Root:"+str(s[x]))
    ##return globlist
    for i in range(1,len(globlist)):
        if globlist[i] == 0:
            return (i-1)*n
    return (i*n)


"""
Functions that combine everything for a quick test of number n
"""
##depreciated
def oldquicktest(n,upper):
    s = betterlist(n,primes(upper))
    a = bettersum(n,s)
    return maxsum(n,a)

##depreciated
def quicktest(n,upper):
    s = betterlist(n,primes(upper))
    return fastersum(n,s,upper*5)

def smalltest(n,upper,q):
    s = betterlist(n,primes(upper))
    return smallersum(n,s,upper*5,q)

def smalltest_wrapper(arg):
    output = smalltest(arg[0],arg[1],arg[2])
    arg[2].put([arg[0],output])
    return output

##bad
def multitest(n,upper):
    s = betterlist(n,primes(upper))
    return multisum(n,s,upper*5)

##bad
def mfastertest(n,upper):
    s = betterlist(n,primes(upper))
    return mfastersum(n,s,upper*5)

##Python, Y U NO pass by reference?
def reftest(n,upper):
    s = betterlist(n,primes(upper))
    return refsum(n,s,upper*5)

"""
Test a bunch of n
"""
##good for small batches
def batch(start, stop, size):
    p = primes(size)
    for n in range(start,stop):
        a = copy.copy(p)
        s = betterlist(n,a)
        print(smallersum(n,s,size*5))

##good for big batches, but doesn't show progress
def asyncbatch(start, stop, size):
    pool = Pool(PROCESSES)
    return pool.map_async(smalltest_wrapper, [(n,size) for n in range(start,stop)])

def multibatch(start, stop, size):
    pool = Pool(PROCESSES)
    a = pool.map(smalltest_wrapper, [(n,size) for n in range(start,stop)])
    for x in a:
        print (str(start) + ' ' + str(x))
        start += 1
    print(a)

##Now shows Progress! Uses Manager and Queue, breaks some older functions
def betterbatch(start, stop, size):
    print("Using", PROCESSES, "Cores")
    manager = Manager()
    q = manager.Queue()
    pool = Pool(PROCESSES)
    a = pool.map_async(smalltest_wrapper, [(n,size,q) for n in range(start,stop)])
    pool.close()
    reported = stop-start+1
    awake = 0
    while (True):
        if (a.ready()): break
        remaining = a._number_left
        if (remaining != reported):
            print ("Waiting for", remaining, "tasks to complete...")
            reported = remaining
        elif (awake > 10):
            print ("Waiting for", remaining, "tasks to complete... I'm Awake!")
            awake = 0
        else:
            awake += 1
        while not q.empty():
            print(q.get())
        time.sleep(5)
    b = a.get()
    pool.join()
    ##for x in b:
        ##print (str(start) + ' ' + str(x))
        ##start += 1
    print(b)
