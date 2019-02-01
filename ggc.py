# Eric Lesiuta
# Program for testing my generalization of Goldbach's Conjecture


def coprimelist(n, stop):
    """returns the minimal list of coprimes where each element modulo n = 1.
    every number that is a multiple of n and > n**2 can be written as the sum
    of n items from this list.
    """
    coprimes = [n+1]
    for i in range(n+1, stop, n):
        coprime = True
        for c in coprimes:
            if gcd(i, c) != 1:
                coprime = False
        if coprime:
            coprimes.append(i)
    return coprimes


def createcomet(n, stop, coprimes):
    """generates a comet for the generalization using multiples of n, for all
    numbers up to stop.
    output comet[i] is the number of ways n*i can be represented as a sum of n
    coprimes from coprimelist.
    """
    # unrolled version of the recursive function
    cd = 1  # current array depth
    md = int(n)  # max depth = n
    sums = [0]*(n+1)  # sums (at each depth)
    index = [0]*(n+1)  # index (at each depth)
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


def factor(n, coprimes):
    """factorization without duplicates."""
    n = int(n)
    p = coprimes[:]
    if 1 in p:
        p.remove(1)
    factors = []
    sqrtn = int(n**0.5) + 1
    for x in p:
        if n % x == 0:
            factors.append(x)
            n //= x
        while n % x == 0:
            n //= x
        if ((n == 1) | (x > sqrtn)):
            break
    if n != 1:
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


def fastcoprimelist(n, primes):
    """returns the minimal list of coprimes where each element modulo n = 1.
    every number that is a multiple of n and > n**2 can be written as the sum
    of n items from this list.
    optimized to run quickly for generating longer lists of coprimes when
    given a list of primes.
    """
    primes = primes[:]
    maxprime = primes[-1]
    # according to my rules, each number must have a %n == 1 therefore these
    # numbers or any multiples can't be used
    # eg for goldbach's conjecture, this bit of code will remove 2, which only
    # affects 4 = 2 + 2
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


def writecomet(n, comet):
    """writes the comet/distribution with each entry on a new line"""
    f = open("n="+str(n)+".txt", "w")
    for x in comet:
        f.write(str(x)+"\n")
    f.close()


def plotcomet(n, stop, comet):
    """plots the comet/distribution, the number of ways 'x' can be written as
    a sum of 'n' coprimes from the set generated with coprimelist"""
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
    coprimes = coprimelist(n, stop)
    comet = createcomet(n, stop, coprimes)
    writecomet(n, comet)
    plotcomet(n, stop, comet)


if __name__ == "__main__":
    import argparse
    coprimes = None
    comet = None
    readme = ("Goldbach's conjecture originally states every integer greater than 2 (or 5 if 1\n"
              "is not considered to be prime) can be written as the sum of 3 primes or\n"
              "equivalently every even integer greater than 2 can be written as the sum of 2\n"
              "primes.\n\n"
              "In this generalization, every integer greater than n squared that is a multiple\n"
              "of n can be written as the sum of n coprimes from the minimal set of coprime\n"
              "numbers where each number of the set modulo n is 1.\n\n"
              "When n = 2, this is equivalent to Goldbach's conjecture, with the minimal set of\n"
              "coprime numbers simply being the set of prime numbers with the exception of 2\n"
              "being removed since 2 mod 2 = 0.\n\n"
              "Since the only even number that can be written as a sum using 2 is 4 = 2 + 2,\n"
              "this has no effect on any other number.")

    parser = argparse.ArgumentParser(description="Test a generalization of Goldbach's conjecture")
    parser.add_argument("--readme", action="store_true",
                        help="displays the readme")
    parser.add_argument("-n", type=int, default=2, metavar="N",
                        help="integer n used for the generalization, see readme for explanation (default: 2)")
    parser.add_argument("-s", type=int, default=100, metavar="STOP",
                        help="test up to stop (default: 100)")
    parser.add_argument("-cp", "--coprimes", action="store_true",
                        help="returns the list of coprimes")
    parser.add_argument("-c", "--comet", action="store_true",
                        help="returns the number of ways 'x' can be written as a sum of 'n' coprimes")
    parser.add_argument("-w", "--writecomet", action="store_true",
                        help="writes comet 'n=N.txt' in the current directory")
    parser.add_argument("-p", "--plot", action="store_true",
                        help="saves plot 'n=N.png' of the comet in the current directory")
    args = parser.parse_args()

    if (args.readme):
        print(readme)

    if (args.coprimes):
        coprimes = coprimelist(args.n, args.s)
        print(coprimes)

    if (args.comet):
        if (coprimes is None):
            coprimes = coprimelist(args.n, args.s)
        comet = createcomet(args.n, args.s, coprimes)
        print(comet)

    if (args.writecomet):
        if (coprimes is None):
            coprimes = coprimelist(args.n, args.s)
        if (comet is None):
            comet = createcomet(args.n, args.s, coprimes)
        writecomet(args.n, comet)

    if (args.plot):
        if (coprimes is None):
            coprimes = coprimelist(args.n, args.s)
        if (comet is None):
            comet = createcomet(args.n, args.s, coprimes)
        plotcomet(args.n, args.s, comet)

    if (not (args.readme or args.coprimes or args.comet or args.writecomet or args.plot)):
        parser.print_help()
