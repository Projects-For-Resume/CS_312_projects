import random
import sys

# This may come in handy...
from fermat import miller_rabin

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def euclid(a,b):
    if b == 0:
        return a
    return euclid(b, a%b)

def find_e(E, p, q):
    for e in E:
        if euclid(e, (p-1)*(q-1)) == 1:
            return e

# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    """
    The Extended Euclid algorithm
    Returns x, y , d such that:
    - d = GCD(a, b)
    - ax + by = d

    Note: a must be greater than b
    """
    if a < b:
        raise ValueError("a cannot be less than b")

    x: int = 0
    y: int = 0
    z: int = 0

    if b == 0:
        return (1,0,a)
    x, y, z = ext_euclid(b, a%b)
    return (y, (x - (a//b)*y), z)


# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
     specified bit length.
    """
    result: str = "composite"
    prime: int = 0

    while result == "composite":
        prime = random.getrandbits(bits)
        if prime % 2 == 0:
            continue
        if miller_rabin(prime, 10) == "prime":
            result = "prime"

    return prime


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Return N, e, d
    - N must be the product of two random prime numbers p and q
    - e and d must be multiplicative inverses mod (p-1)(q-1)
    """
    p:int = generate_large_prime(bits)
    q:int = generate_large_prime(bits)
    N: int = p * q

    d_rsa: int = 0
    e_rsa: int = 0
    for e in primes:
        holder, d_rsa, check = ext_euclid(((p-1)*(q-1)), e)
        if check == 1:
            e_rsa = e
            while d_rsa < 0:
                d_rsa += (p-1)*(q-1)
            break

    return N, e_rsa, d_rsa
