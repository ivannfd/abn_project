import numpy as np
import math


def get_a_posteriori_estimates(atomic_count, conjunct_probs, evidence_data):
    n = 2 ** atomic_count

    I = np.array([[1, -1], [0, 1]])
    In = np.array([[1, -1], [0, 1]])
    J = np.array([[1, 1], [0, 1]])
    Jn = np.array([[1, 1], [0, 1]])

    Hpl = np.array([[0, 0], [0, 1]])
    Hmi = np.array([[1, 0], [0, 0]])
    Hn = np.array([[1, 0], [0, 1]])

    H = np.array([[0, 0], [0, 0]])

    k = 2

    while k < n:
        In = np.kron(In, I)
        Jn = np.kron(Jn, J)
        k *= 2
    P = np.zeros((n, 1))

    P[0][0] = 1

    cou = 0
    for i in range(1, n):
        x = float(conjunct_probs[cou])
        cou += 1
        P[i][0] = x  # считываем оценки

    S = []

    cou = 0
    for i in range(int(math.log2(n))):  # считываем свидетельство
        x = evidence_data[cou]
        S.append(x)
        cou += 1

    if S[int(math.log2(n)) - 1] == '-':
        H = Hn
    if S[int(math.log2(n)) - 1] == '1':
        H = Hpl
    if S[int(math.log2(n)) - 1] == '0':
        H = Hmi

    for i in range(int(math.log2(n) - 2), -1, -1):
        if S[i] == '-':
            H = np.kron(H, Hn)
        if S[i] == '1':
            H = np.kron(H, Hpl)  # строим матрицу H
        if S[i] == '0':
            H = np.kron(H, Hmi)

    K = np.matmul(Jn, H)  # строим матрицу T
    T = np.matmul(K, In)
    R = np.matmul(T, P)
    return R / R[0][0]


if __name__ == '__main__':
    print("Введите кол-во атомов: ")
    k = int(input())  # 2

    print("Введите в строчку вероятностные оценки конъюнктов: ")
    frag1 = input()
    frag2 = frag1.split()  #

    print("В строчку введите 1, если утвержение под этим номером истинно, 0 если ложно, - если нет информации: ")
    svid1 = input()
    svid2 = svid1.split()
    print("Получившиеся оценки апостериорных вероятностей:")
    print(get_a_posteriori_estimates(k, frag2, svid2))
