from math import ceil
import pandas as pd
import matplotlib.pyplot as plt

F = 15000
us = 30
di = 2

Ns = [10, 100, 1000]
us_peers = [0.3, 0.7, 2.0]

T_cs = []

for N in Ns:
    t = max(
        N * F / us, 
        F / di
    )
    T_cs.append(t)

T_p2p = {}

for u in us_peers:
    times = []

    for N in Ns:
        t = max(
            F / us,
            F / di,
            (N * F) / (us + N * u)
        )

        times.append(t)

    T_p2p[u] = times


print("Клиент-сервер")
for N, t in zip(Ns, T_cs):
    print(f"N = {N}: {t:.2f} c")

print("\nP2P")

for u in us_peers:
    print(f"\nu = {u} Мбит/с")

    for N, t in zip(Ns, T_p2p[u]):
        print(f"N = {N}: {t:.2f} c")


plt.figure(figsize=(10, 6))

plt.plot(
    Ns,
    T_cs,
    marker='o',
    linewidth=2,
    label='Клиент-сервер'
)

for u in us_peers:
    plt.plot(
        Ns,
        T_p2p[u],
        marker='o',
        linewidth=2,
        label=f'P2P, u = {u} Мбит/с'
    )

plt.xscale('log')
plt.xlabel('Количество пиров')
plt.ylabel('Минимальное время раздачи (с)')
plt.title('Минимальное время раздачи')
plt.grid(True)
plt.legend()
plt.show()