import time
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def rsa_key_generation(bit_length, iterations=10):
    start_time = time.perf_counter()
    key = None
    for _ in range(iterations):
        key = RSA.generate(bit_length)
    elapsed_time = (time.perf_counter() - start_time) / iterations
    return key, elapsed_time

def rsa_encrypt(key, message, iterations=10):
    cipher = PKCS1_OAEP.new(key.publickey())
    start_time = time.perf_counter()
    encrypted_message = None
    for _ in range(iterations):
        encrypted_message = cipher.encrypt(message)
    elapsed_time = (time.perf_counter() - start_time) / iterations
    return encrypted_message, elapsed_time

def rsa_decrypt(key, encrypted_message, iterations=10):
    cipher = PKCS1_OAEP.new(key)
    start_time = time.perf_counter()
    decrypted_message = None
    for _ in range(iterations):
        decrypted_message = cipher.decrypt(encrypted_message)
    elapsed_time = (time.perf_counter() - start_time) / iterations
    return decrypted_message, elapsed_time

def add_regression_line(ax, x, y, color, label):
    # Regressão linear
    slope, intercept, _, _, _ = stats.linregress(x, y)
    line_x = x
    line_y = slope * line_x + intercept
    
    # Desenhar reta de regressão
    ax.plot(line_x, line_y, color=color, label=label, linewidth=2, zorder=2)  # zorder para manter a linha à frente
    return slope, intercept

def measure_efficiency(bit_length, message, repetitions=100, iterations=10):
    print(f"Medição de eficiência para {bit_length} bits iniciada...")

    key_gen_times = []
    encryption_times = []
    decryption_times = []
    total_times = []

    for _ in range(repetitions):
        key, key_gen_time = rsa_key_generation(bit_length, iterations)
        encrypted_message, encryption_time = rsa_encrypt(key, message, iterations)
        decrypted_message, decryption_time = rsa_decrypt(key, encrypted_message, iterations)

        assert decrypted_message == message, "Erro na decifração"

        key_gen_times.append(key_gen_time)
        encryption_times.append(encryption_time)
        decryption_times.append(decryption_time)
        total_times.append(key_gen_time + encryption_time + decryption_time)

    plt.figure(figsize=(14, 8))

    metrics = [
        (key_gen_times, "Tempo de Geração de Chave", "blue", "red"),
        (encryption_times, "Tempo de Cifração", "orange", "cyan"),
        (decryption_times, "Tempo de Decifração", "green", "magenta"),
        (total_times, "Tempo Total", "red", "blue")
    ]

    for i, (times, title, point_color, line_color) in enumerate(metrics, 1):
        ax = plt.subplot(2, 2, i)
        x = range(1, repetitions + 1)
        ax.scatter(x, times, color=point_color, label=title, zorder=1)
        add_regression_line(ax, pd.Series(x), pd.Series(times), line_color, "Regressão Linear")
        ax.set_title(title)
        ax.set_xlabel("Repetição")
        ax.set_ylabel("Tempo (s)")
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.savefig(f"resultados_RSA_{bit_length}_graficos_com_regressao.png")
    plt.close()  # Fecha o gráfico para permitir continuar a execução

    data = {
        "Repetição": list(range(1, repetitions + 1)),
        "Tempo de Geração de Chave (s)": key_gen_times,
        "Tempo de Cifração (s)": encryption_times,
        "Tempo de Decifração (s)": decryption_times,
        "Tempo Total (s)": total_times,
    }

    data_df = pd.DataFrame(data)

    summary = {
        "Métrica": ["Média", "Desvio Padrão", "Coeficiente de Variação (%)"],
        "Geração de Chave": [pd.Series(key_gen_times).mean(), pd.Series(key_gen_times).std(), (pd.Series(key_gen_times).std() / pd.Series(key_gen_times).mean()) * 100],
        "Cifração": [pd.Series(encryption_times).mean(), pd.Series(encryption_times).std(), (pd.Series(encryption_times).std() / pd.Series(encryption_times).mean()) * 100],
        "Decifração": [pd.Series(decryption_times).mean(), pd.Series(decryption_times).std(), (pd.Series(decryption_times).std() / pd.Series(decryption_times).mean()) * 100],
        "Tempo Total": [pd.Series(total_times).mean(), pd.Series(total_times).std(), (pd.Series(total_times).std() / pd.Series(total_times).mean()) * 100],
    }

    summary_df = pd.DataFrame(summary)
    return data_df, summary_df

def main():
    message = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@"
    bit_lengths = [1024, 2048, 3072, 4096]
    writer = pd.ExcelWriter("resultados_RSA_α.xlsx", engine="xlsxwriter")

    for bit_length in bit_lengths:
        data_df, summary_df = measure_efficiency(bit_length, message)

        data_df.to_excel(writer, sheet_name=f"{bit_length}_Dados", index=False)
        summary_df.to_excel(writer, sheet_name=f"{bit_length}_Estatísticas", index=False)

    writer.close()
    print("Resultados salvos em 'resultados_RSA_α.xlsx'")

if __name__ == "__main__":
    main()
