import random
import time
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
from math import sqrt

#Este código foi feito antes do algoritmo α, por conta disso pode haver diferenças, especialmente em relação a medição de tempo e ao salvamento na planilha.

def crivo(bits):
    n = (1 << bits) - 1  # 2^bits - 1
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(sqrt(n)) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
    return [p for p in range(2, n + 1) if is_prime[p]]

def text_to_ascii(text):
    return [ord(char) for char in text]

def ascii_to_text(ascii_values):
    return ''.join(chr(value % 256) for value in ascii_values)

def euclides(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, t):
    gcd, x, _ = euclides(e, t)
    if gcd != 1:
        raise ValueError("Inverso modular não existe.")
    return x % t

def rsa_encrypt_decrypt(p, q, message):
    n = p * q
    t = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, t)

    ascii_values = text_to_ascii(message)
    encrypted_values = [pow(value, e, n) for value in ascii_values]
    decrypted_values = [pow(value, d, n) for value in encrypted_values]
    decrypted_message = ascii_to_text(decrypted_values)

    return encrypted_values, decrypted_message

def measure_rsa_performance(bits, message):
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)
    while p == q:
        q = generate_prime_number(bits)

    times = {"keygen": 0, "encrypt": 0, "decrypt": 0}
    repetitions = 30

    start = time.perf_counter()
    n = p * q
    t = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, t)
    times["keygen"] += (time.perf_counter() - start)

    for _ in range(repetitions):
        ascii_values = text_to_ascii(message)

        start = time.perf_counter()
        encrypted_values = [pow(value, e, n) for value in ascii_values]
        times["encrypt"] += (time.perf_counter() - start)
      
        start = time.perf_counter()
        decrypted_values = [pow(value, d, n) for value in encrypted_values]
        times["decrypt"] += (time.perf_counter() - start)

    for key in times:
        times[key] /= repetitions

    return times

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << (length - 1)) | 1
    return p

def is_prime_miller_rabin(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_number(length):
    p = 4
    while not is_prime_miller_rabin(p):
        p = generate_prime_candidate(length)
    return p

def calculate_statistics(data):
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    coef_var = (std_dev / mean) * 100 if mean != 0 else 0
    relative_errors = [(abs(x - mean) / mean) * 100 for x in data]
    relative_mean_error = np.mean(relative_errors)
    relative_max_error = np.max(relative_errors)
    conf_interval = 1.96 * (std_dev / sqrt(len(data)))
    return {
        "mean": mean,
        "std_dev": std_dev,
        "coef_var": coef_var,
        "rel_mean_err": relative_mean_error,
        "rel_max_err": relative_max_error,
        "conf_lower": mean - conf_interval,
        "conf_upper": mean + conf_interval
    }

def save_to_excel(results, filename="rsa_results.xlsx"):
    workbook = xlsxwriter.Workbook(filename)

    sheet_times = workbook.add_worksheet("Tempos")
    sheet_times.write_row(0, 0, ["Bits", "Operação", "Tempos (s)"])

    row = 1
    for bits, data in results.items():
        for operation, times in data.items():
            for time in times:
                sheet_times.write_row(row, 0, [bits, operation, time])
                row += 1

    sheet_stats = workbook.add_worksheet("Estatísticas")
    sheet_stats.write_row(0, 0, ["Bits", "Operação", "Média", "Desvio Padrão", "Coef. Variação (%)", "Erro Relativo Médio (%)", "Erro Relativo Máximo (%)", "IC Inferior", "IC Superior"])

    row = 1
    for bits, data in results.items():
        for operation, times in data.items():
            stats = calculate_statistics(times)
            sheet_stats.write_row(row, 0, [
                bits, operation, stats["mean"], stats["std_dev"], stats["coef_var"],
                stats["rel_mean_err"], stats["rel_max_err"], stats["conf_lower"], stats["conf_upper"]
            ])
            row += 1

    workbook.close()

def main():
    message = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@"
    bit_lengths = [1024, 2048, 4096]

    results = {length: {"keygen": [], "encrypt": [], "decrypt": []} for length in bit_lengths}

    for bits in bit_lengths:
        for _ in range(10):  # 10 repetições
            times = measure_rsa_performance(bits, message)
            for key in times:
                results[bits][key].append(times[key])

    save_to_excel(results)

    for bits in bit_lengths:
        plt.scatter([bits] * len(results[bits]["encrypt"]), results[bits]["encrypt"], label=f"Encrypt {bits} bits")
    plt.title("Desempenho da Cifração RSA")
    plt.xlabel("Tamanho da Chave (bits)")
    plt.ylabel("Tempo (segundos)")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
