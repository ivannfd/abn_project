import numpy as np
import math
print("Введите кол-во атомов: ")
k = int(input())   #кол-во атомов вo фрагменте знаний

n = 2 ** k

I = np.array([[1 ,-1],[0, 1]])
In = np.array([[1 ,-1],[0, 1]])
J = np.array([[1,1], [0,1]])
Jn = np.array([[1,1], [0,1]])


Hpl = np.array([[0 ,0],[0, 1]])
Hmi = np.array([[1 ,0],[0, 0]])
Hn = np.array([[1 ,0],[0, 1]])

H =  np.array([[0 ,0],[0, 0]])


k = 2

while k<n:
    In = np.kron(In,I)
    Jn = np.kron(Jn,J)
    k*=2
P=np.zeros((n,1))

P[0][0] = 1
print("Введите в строчку оценки вероятности истинности конъюнктов: ")
frag1  = input()
frag2=frag1.split()
cou = 0
for i in range(1,n):
    x =float(frag2[cou])
    cou+=1
    P[i][0]=x                #считываем оценки

S=[]
print("В строчку введите 1, если атом получил положительное означивание, 0 если отрицательное означивание, - если нет информациии (нумерация атомов начинается с 0): ")
svid1  = input()
svid2  = svid1.split()
cou = 0
for i in range (int(math.log2(n))):   #считываем свидетельство
    x=svid2[cou]
    S.append(x)
    cou+=1


if S[int(math.log2(n))-1]=='-':
    H=Hn
if S[int(math.log2(n))-1] == '1':
    H = Hpl
if S[int(math.log2(n))-1]=='0':
    H = Hmi



for i in range(int(math.log2(n)-2),-1, -1):
    if S[i]=='-':
        H = np.kron(H,Hn)
    if S[i]=='1':
        H = np.kron(H,Hpl)                             #строим матрицу H
    if S[i] == '0':
            H = np.kron(H, Hmi)


K = np.matmul(Jn,H)                                   #строим матрицу T
T = np.matmul(K,In)
R=np.matmul(T,P)
print("Получившиеся оценки апостериорных вероятностей:")
print(R/R[0][0])



















