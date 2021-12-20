import math
from typing import List

import numpy as np


# теперь разберемся с номером i
# TODO: rename function and maybe arguments
def fun(v, w):
    k = list((bin(int(v))))
    del k[0]
    del k[0]
    s = len(k)
    for i in range(s):
        k[i] = int(k[i])
    while s < w:
        k.insert(0, 0)
        s += 1
    return k


# наконец мы можем написать функцию Gind
def gind(k, m):
    for i in range(len(m) - 1, -1, -1):
        if m[i] == 0:
            g = len(m) - 1 - i
            k.insert(len(k) - g, 0)

    return k


# TODO: rename function and arguments
def get_something(number_of_atoms: int, frag2: List[str], svid2: List[str], frag4: List[str]):
    n1 = 2 ** number_of_atoms

    I = np.array([[1, -1], [0, 1]])
    In = np.array([[1, -1], [0, 1]])
    Ik = np.array([[1, -1], [0, 1]])
    J = np.array([[1, 1], [0, 1]])
    Jn = np.array([[1, 1], [0, 1]])

    Hpl = np.array([[0, 0], [0, 1]])
    Hmi = np.array([[1, 0], [0, 0]])
    Hn = np.array([[1, 0], [0, 1]])

    H = np.array([[0, 0], [0, 0]])
    Y = np.zeros((n1, 1))

    k = 2

    while k < n1:
        In = np.kron(In, I)
        Jn = np.kron(Jn, J)
        k *= 2

    P1 = np.zeros((n1, 1))

    P1[0][0] = 1
    cou = 0
    for i in range(1, n1):
        x = float(frag2[cou])
        P1[i][0] = x
        cou += 1  # считываем оценки

    S = []
    k = 0
    n2 = 0

    cou = 0
    for i in range(int(math.log2(n1))):  # какие атомы мы берем в наше свидительство
        x = svid2[cou]
        cou += 1
        if x == '+':
            S.append(i)
            n2 += 1

    P2 = np.zeros((2 ** n2, 1))

    P2[0][0] = 1

    cou = 0
    for i in range(1, 2 ** n2):  # считываем само свидительство
        x = float(frag4[cou])
        P2[i][0] = x
        cou += 1

    # строим I*P
    for i in range(1, n2):
        Ik = np.kron(Ik, I)

    U = np.matmul(Ik, P2)

    # теперь начинаем обработку!

    # вначале получим m
    j = 0
    i = 0
    M = []
    while j < n2:
        if i == S[j]:
            M.insert(0, 1)
            j += 1
            i += 1
        else:
            M.insert(0, 0)
            i += 1

    while i < (math.log2(n1)):
        M.insert(0, 0)
        i += 1

    for i in range(0, 2 ** n2):
        q1 = fun(i, n2)
        q2 = fun(2 ** n2 - i - 1, n2)
        i1 = gind(q1, M)
        j1 = gind(q2, M)

        if j1[0] == 1:
            H = Hmi
        if i1[0] == 1:
            H = Hpl

        if (j1[0] == 0) and (i1[0] == 0):
            H = Hn

        for j in range(1, int(math.log2(n1))):  # cтроим матрицу H
            if j1[j] == 1:
                H = np.kron(H, Hmi)
            if i1[j] == 1:
                H = np.kron(H, Hpl)
            if (j1[j] == 0) and (i1[j] == 0):
                H = np.kron(H, Hn)

        K = np.matmul(Jn, H)  # строим матрицу T
        T = np.matmul(K, In)
        R = np.matmul(T, P1)
        Z = R * U[i] / R[0]
        Y = np.add(Y, Z)

    return Y


def main() -> None:
    number_of_atoms = int(input("Введите количество атомов:\n"))

    # TODO: rename
    frag2 = input("Введите в строчку оценки вероятности истинности конъюнктов:\n").split()

    # TODO: rename
    svid2 = input(
        "В строчку введите '+', если атом присутствует в свидетельстве, '-' если нет. "
        "Порядковый номер ввода соответствует номеру атома (нумерация атомов начинается с 0):\n"
    ).split()

    # TODO: rename
    frag4 = input(
        "Введите в строчку оценки вероятности истинности конъюнктов, которые входят в наше свидетельство:\n"
    ).split()

    print("Получившиеся оценки апостериорных вероятностей:")
    print(get_something(number_of_atoms, frag2, svid2, frag4))


if __name__ == "__main__":
    main()
