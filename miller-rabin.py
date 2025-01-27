def is_prime_fermat(n, k=3):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def is_prime_miller_rabin(n, k=3):
    if not is_prime_fermat(n, k):
        return False
    if n <= 3:
        return True

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << (length - 1)) | 1
    return p

def generate_prime_number(length):
    p = 4
    while not is_prime_miller_rabin(p):
        p = generate_prime_candidate(length)
    return p
