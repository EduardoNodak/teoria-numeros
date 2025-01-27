def crivo(n):
    numeros = list(range(2, n+1))
    is_prime = [True] * (n-1)
    maximo_calcula = floor(numeros[-1] ** (1/2))
    for i in range(2, maximo_calcula + 1):
        for j in range(i*i, n+1, i):
            if i != j:
                if j % i == 0:
                    is_prime[j-2] = False
    primos = [numeros[i] for i,j in enumerate(is_prime) if j == True]
    return primos
