##Alternate way of writing combinations recursively, meant mostly to test logic respective to GB5
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

PROCESSES = cpu_count()

"""
Prime Number Functions
"""

def pf (n,p):
    ##prime factorization (modified to get rid of duplicates)
    ##returns prime factors of n
    ##input p is a list of prime numbers
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

def primes(e):
    ##returns all the primes <= e
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
Functions that make my list of primes and coprimes
"""
##good, need to use something other than python to improve further
def betterlist(n, primes):
    ##makes the set of coprimes that can be used to sum to any number multiple of n, requires list of primes (size depends on how much to test)
    maxprime = primes[-1]
    p = copy.copy(primes)

    ##eg for goldbach's conjecture, this bit of code will remove 2, which only affects 4 = 2 + 2
    ##according to my rules though, the number must have a %n == 1 therefore these numbers or any multiples can't be used
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
    coprimes.remove(1)
    return coprimes

"""
Functions that check which numbers can be written as a sum from my list
"""
##SINGLE PROCESS
##AHHHHHH THIS LOOKS DISGUSTING BUT I DONT KNOW HOW ELSE TO DO THIS
##currently the best version
global globlist

def combinations(cd, md, sum, i, l, q):
    ##returns sum of combinations
    ##current depth, max depth, sum, index, list, multi threaded queue
    global globlist
    for x in range(i, len(l)):
        if cd < md:
            combinations(cd+1,md,sum+l[x],x,l,q)
        else:
            try:
                globlist[(sum+l[x])//md] += 1
            except:
                q.put("WARNING: could not appent to "+ str(int((sum+l[x])/md)));

def smallersum(n, s, upper, q):
    ##creates lis of e that can be written as the sum of n numbers from set s
    ##uses my own function for combinations so they don't all stay stored in memory
    global globlist
    globlist = [0]*upper
    combinations(1,n,0,0,s,q)
    ##return globlist
    for i in range(1,len(globlist)):
        if globlist[i] == 0:
            return (i-1)*n
    return (i*n)


"""
Functions that combine everything for a quick test of number n
"""
def smalltest(n,upper,q):
    global globlist;
    s = betterlist(n,primes(upper))
    sums = smallersum(n,s,upper*5,q)
    # Write the globallist before we return the value
    fh = open(str(n)+"_GB7.txt","w");
    for glob in globlist:
        fh.write(str(glob)+"\n")
    fh.close();
    return sums

def smalltest_wrapper(arg):
    output = smalltest(arg[0],arg[1],arg[2])
    arg[2].put([arg[0],output])
    return output

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
        if (a.ready()): break
        time.sleep(10)
    b = a.get()
    pool.join()
    ##for x in b:
        ##print (str(start) + ' ' + str(x))
        ##start += 1
    print(b)
"""
Main
"""
if __name__ == '__main__':
    ##any parallel processes can only be run here (as defined by Python specification)
    ##Besides setting these numbers, also set time.sleep, recursion depth, frequency of debug info (ctrl+f debug)
    pass
    start = timeit.time.time()
    ##betterbatch(2,4,10000)
    manager = Manager()
    q = manager.Queue()
    smalltest(6,500,q)
    print (timeit.time.time() - start)
