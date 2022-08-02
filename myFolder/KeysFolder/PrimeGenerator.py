import random

def primesInRange(x,y) :

    prime_list=[]
    for n in range(x,y):
        is_prime = True

        for num in range(2,n):
            if n%num == 0:
                is_prime = False
        if is_prime:
            prime_list.append(n)

    return prime_list

def generateTwoPrimes() :
    pMinPrime = 101
    pMaxPrime = 200
    pCachedPrimes = primesInRange(pMinPrime,pMaxPrime)
    p = random.choice([i for i in pCachedPrimes if pMinPrime<i<pMaxPrime])
    # print("PrimeGenerator give Random# p :")
    # print(p)
    qMinPrime = 201
    qMaxPrime = 300
    qCachedPrimes = primesInRange(qMinPrime,qMaxPrime)
    q = random.choice([i for i in qCachedPrimes if qMinPrime<i<qMaxPrime])
    # print("PrimeGenerator give Random# q :")
    # print(q)
    return p,q