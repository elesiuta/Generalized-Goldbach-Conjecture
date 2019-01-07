# Generalized Goldbach Conjecture

A script to test my generalization of Goldbach's Conjecture.

The conjecture originally states every integer greater than 2 (or 5 if 1 is not considered to be prime) can be written as the sum of 3 primes or equivalently every even integer greater than 2 can be written as the sum of 2 primes.

In my generalization, every integer greater than n squared that is a multiple of n can be written as the sum of n coprimes from the minimal set of coprime numbers where each number of the set modulo n is 1.

When n = 2, this is equivalent to Goldbach's conjecture, with the minimal set of coprime numbers simply being the set of prime numbers with the exception of 2 being removed since 2 mod 2 = 0.

Since the only even number that can be written as a sum using 2 is 4 = 2 + 2, this has no effect on any other number.

See the code for a clearer and more precise description, and to test it for yourself.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2525427.svg)](https://doi.org/10.5281/zenodo.2525427)
