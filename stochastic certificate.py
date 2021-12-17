import numpy as np
import math
print("Введите кол-во атомов:")
l = int(input())   #кол-во атомов
n1=2**l

I = np.array([[1 ,-1],[0, 1]])
In = np.array([[1 ,-1],[0, 1]])
Ik = np.array([[1 ,-1],[0, 1]])
J = np.array([[1,1], [0,1]])
Jn = np.array([[1,1], [0,1]])


Hpl = np.array([[0 ,0],[0, 1]])
Hmi = np.array([[1 ,0],[0, 0]])
Hn = np.array([[1 ,0],[0, 1]])

H =  np.array([[0 ,0],[0, 0]])
Y =  np.zeros((n1,1))

k = 2

while k<n1:
    In = np.kron(In,I)
    Jn = np.kron(Jn,J)
    k*=2
P1=np.zeros((n1,1))

P1[0][0] = 1
print("Введите в строчку оценки вероятности истинности конъюнктов: ")
frag1  = input()
frag2=frag1.split()
cou = 0
for i in range(1,n1):
    x = float(frag2[cou])
    P1[i][0]=x
    cou+=1    #считываем оценки


S=[]
k=0
n2=0
print("В строчку введите +, если атом присутствует в свидетельстве,- если нет. Порядковый номер ввода соответствует номеру атома (нумерация атомов начинается с 0): ")
svid1  = input()
svid2  = svid1.split()
cou = 0
for i in range (int(math.log2(n1))):   #какие атомы мы берем в наше свидительство
    x=svid2[cou]
    cou+=1
    if x=='+':
        S.append(i)
        n2+=1


P2=np.zeros((2**n2,1))

P2[0][0] = 1
print("Введите в строчку оценки вероятности истинности конъюнктов, которые входят в наше свидетельство: ")

frag1 = input()
frag2=frag1.split()
cou = 0
for i in range(1,2**n2):              #считываем само свидительство
    x = float(frag2[cou])
    P2[i][0]=x
    cou+=1


#строим I*P
for i in range (1,n2):
    Ik = np.kron(Ik,I)

U=np.matmul(Ik,P2)


#теперь начинаем обработку!

#вначале получим m
j=0
i=0
M=[]
while j<n2:
     if i==S[j]:
         M.insert(0,1)
         j+=1
         i+=1
     else:
        M.insert(0, 0)
        i+=1

while i<(math.log2(n1)):
       M.insert(0, 0)
       i+=1

#теперь разберемся с номером i

def fun(v,w):
    k = list((bin(int(v))))
    del k[0]
    del k[0]
    s=len(k)
    for i in range (s):
        k[i] = int(k[i])
    while (s<w):
        k.insert(0,0)
        s+=1
    return(k)


#наконец мы можем написать функцию Gind
def Gind (k,m):
    for i in range (len(m)-1,-1,-1):
        if m[i]==0:
            g=len(m)-1-i
            k.insert(len(k)-g,0)

    return(k)


for i in range(0,2**n2):
   q1 = fun(i,n2)
   q2 = fun(2**n2-i-1,n2)
   i1 = Gind(q1,M)
   j1 = Gind(q2,M)

   if j1[0]==1:
       H=Hmi
   if i1[0]==1:
       H=Hpl

   if (j1[0]==0) and (i1[0]==0):
       H=Hn


   for j in range (1,int(math.log2(n1))):               #cтроим матрицу H

       if j1[j] == 1:
           H =np.kron(H,Hmi)
       if i1[j] == 1:
           H =np.kron(H,Hpl)

       if (j1[j] == 0) and (i1[j] == 0):
           H = np.kron(H,Hn)

   K = np.matmul(Jn,H)                                   #строим матрицу T
   T = np.matmul(K,In)
   R = np.matmul(T, P1)
   Z=R*U[i]/R[0]
   Y=np.add(Y,Z)

print("Получившиеся оценки апостериорных вероятностей:")
print(Y)







