def euclides(a, b): 
    if a == 0:
        return b, 0, 1
    mdc, x1, y1 = euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return mdc, x, y
def inverso_multiplicativo(a, m):
    gcd, x, _ = euclides(a, m)
    if gcd != 1:
        raise ValueError("Inverso não existe porque a e m não são coprimos")
    return x % m

def resolve_congruencia(a, C, M): #O(log(M))
    inv_a = inverso_multiplicativo(a, M)
    return (inv_a * C) % M

def TRC(congruences):
    M = 1
    for _, _, M_i in congruences:
        M *= M_i
    x0 = 0
    for a_i, C_i, M_i in congruences:
        n_i = M // M_i
        S_i = inverso_multiplicativo(n_i, M_i)
        b_i = resolve_congruencia(a_i, C_i, M_i)
        x0 += b_i * n_i * S_i
    x0 = x0 % M
    
    return x0

def main():
    print("Solucionador de sistemas de congruências usando o Teorema Chinês do Resto.")
    congruences = []
    while True:
        try:
            a = int(input("Digite o coeficiente a (ou 'sair' para terminar): "))
            C = int(input("Digite o valor C: "))
            M = int(input("Digite o módulo M: "))
            congruences.append((a, C, M))
        except ValueError:
            break
    if len(congruences) == 0:
        print("Nenhuma congruência foi inserida. Saindo.")
        return
    try:
        solution = TRC(congruences)
        product_of_moduli = 1
        for _, _, M_i in congruences:
            product_of_moduli *= M_i
        print(f"A solução para o sistema de congruências é x ≡ {solution} (mod {product_of_moduli})")
    except ValueError as e:
        print(f"Erro: {e}")
if __name__ == "__main__":
    main()
