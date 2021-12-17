import numpy as np
import math
print("Введите кол-во атомов в первом фрагменте знаний: ")
QuantityF1 = int(input())   #кол-во атомов в первом фрагменте знаний
print("Введите кол-во атомов вo втором фрагменте знаний: ")
QuantityF2 = int(input())   #кол-во атомов во втором фрагменте знаний
print("Введите кол-во общих атомов: ")
QuantityGe =int(input())    #кол-во общ

print("Введите в строчку номера общих атомов: ")
frag1 = input()
frag2 = frag1.split()
cou = 0
# их атомов


General=[]

for i in range (QuantityGe):
    x = int(frag2[cou])
    #номера общих атомов
    General.append(x)
    cou+=1

j=0
Com = []


for i in range (0, QuantityF1):

    if j==QuantityGe:
        break
    if i!=General[j] :       #преобразуем общие атомы в последовательность из 0 и 1(длина последоватеьности - кол-во атомов в первом фрагменте знаний)
        Com.insert(0,0)
    if i==General[j]:
         Com.insert(0,1)
         j+=1
    i+=1
for k in range (i, QuantityF1):
      Com.insert(0,0)


n1= 2 ** QuantityF1
n2= 2 ** QuantityF2


I = np.array([[1 ,-1],[0, 1]])
In1 = np.array([[1 , -1], [0, 1]])
In2 = np.array([[1 , -1], [0, 1]])
Ik1 = np.array([[1 , -1], [0, 1]])
Ik2 =np.array([[1 , -1], [0, 1]])
J = np.array([[1,1], [0,1]])
Jn1 = np.array([[1, 1], [0, 1]])
Jn2 = np.array([[1, 1], [0, 1]])

Hpl = np.array([[0 ,0],[0, 1]])
Hmi = np.array([[1 ,0],[0, 0]])
Hn = np.array([[1 ,0],[0, 1]])
H =  np.array([[0 ,0],[0, 0]])

Ap1 =  np.zeros((n1, 1))
Ap2 = np.zeros((n2, 1))

k = 2

while k<n1:
    In1 = np.kron(In1, I)
    Jn1 = np.kron(Jn1, J)
    k*=2


k=2
while k<n2:
    In2 = np.kron(In2, I)
    Jn2 = np.kron(Jn2, J)
    k*=2

Fz1=np.zeros((n1, 1))
Fz1[0][0] = 1

print("Введите в строчку оценки вероятности истинности конъюнктов из первого фрагмента знаний: ")
frag1  = input()
frag2=frag1.split()
cou = 0

for i in range(1,n1):
    x =float(frag2[cou])
    Fz1[i][0]=x                          #считываем оценки первого фрагмента знаний
    cou+=1

Fz2=np.zeros((n2, 1))
Fz2[0][0] = 1

print("Введите в строчку оценки вероятности истинности конъюнктов из второго фрагмента знаний: ")
frag1 = input()
frag2=frag1.split()
cou = 0

for i in range(1, n2):
    x =float(frag2[cou])
    Fz2[i][0]=x                           #считываем оценки второго фрагмента знаний
    cou+=1



S=[]
k=0
QuantitySv=0

print("В строчку введите +, если атом присутствует в свидетельстве,- если нет. Порядковый номер ввода соответствует номеру атома (нумерация атомов начинается с 0): ")
svid1  = input()
svid2  = svid1.split()
cou =0
for i in range (QuantityF1):   #какие атомы мы берем в наше свидительство(первый фрагмент знаний)
    x=svid2[cou]
    cou+=1
    if x=='+':
        S.append(i)
        QuantitySv+=1



Sv1=np.zeros((2 ** QuantitySv, 1))
Sv2= np.zeros((2 ** QuantityGe, 1))
Sv1[0][0] = 1

print("Введите в строчку оценки вероятности истинности конъюнктов, которые входят в наше свидетельство: ")
svid1  = input()
svid2  = svid1.split()
cou =0

for i in range(1, 2 ** QuantitySv):              #считываем само свидительство
    x =float(svid2[cou])
    Sv1[i][0]=x
    cou+=1


for i in range (1, QuantitySv):                   #строим I*P
    Ik1 = np.kron(Ik1, I)

U1=np.matmul(Ik1, Sv1)


for i in range (1, QuantityGe):
    Ik2 = np.kron(Ik2, I)



#теперь начинаем обработку!


#вначале получим M1
j=0
i=0
M1=[]
while j<QuantitySv:
     if i==S[j]:
         M1.insert(0, 1)
         j+=1
         i+=1
     else:
        M1.insert(0, 0)
        i+=1

while i<QuantityF1:
       M1.insert(0, 0)
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


for i in range(0, 2 ** QuantitySv):
   q1 = fun(i, QuantitySv)
   q2 = fun(2 ** QuantitySv - i - 1, QuantitySv)
   i1 = Gind(q1, M1)
   j1 = Gind(q2, M1)

   if j1[0]==1:
       H=Hmi
   if i1[0]==1:
       H=Hpl

   if (j1[0]==0) and (i1[0]==0):
       H=Hn


   for j in range (1,QuantityF1):               #cтроим матрицу H

       if j1[j] == 1:
           H =np.kron(H,Hmi)
       if i1[j] == 1:
           H =np.kron(H,Hpl)

       if (j1[j] == 0) and (i1[j] == 0):
           H = np.kron(H,Hn)

   K = np.matmul(Jn1, H)                                   #строим матрицу T
   T = np.matmul(K, In1)
   R = np.matmul(T, Fz1)
   Z= R * U1[i] / R[0]
   Ap1=np.add(Ap1, Z)
print("Апостериорные вероятности в первом фрагменте знаний:")
print(Ap1)
print("----------------------")

#теперь нужно выбрать только те данные в апостериорном выводе, которые нам нужнны

u =0

for i in range (n1):
    m = fun(i, QuantityF1)
                                      #обработали наше свидетельство
    for j in range(QuantityF1):
        if Com[j]==0 and m[j]==1:
            break
        if j==QuantityF1-1:
           Sv2[u][0]=Ap1[i][0]
           u+=1
    j=0

U2=np.matmul(Ik2, Sv2)
print("Новое сформированное свидетельство:")
print (Sv2)
print("----------------")

#теперь начинаем обработку второго фрагмента!

#вначале получим M2
j=0
i=0
M2=[]
while j<QuantityGe:
     if i==General[j]:
         M2.insert(0, 1)
         j+=1
         i+=1
     else:
        M2.insert(0, 0)
        i+=1

while i<QuantityF2:
       M2.insert(0, 0)
       i+=1


for i in range(0, 2 ** QuantityGe):
   q1 = fun(i, QuantityGe)
   q2 = fun(2 ** QuantityGe - i - 1, QuantityGe)
   i1 = Gind(q1, M2)
   j1 = Gind(q2, M2)

   if j1[0]==1:
       H=Hmi
   if i1[0]==1:
       H=Hpl

   if (j1[0]==0) and (i1[0]==0):
       H=Hn


   for j in range (1, QuantityF2):                     #cтроим матрицу H

       if j1[j] == 1:
           H =np.kron(H,Hmi)
       if i1[j] == 1:
           H =np.kron(H,Hpl)

       if (j1[j] == 0) and (i1[j] == 0):
           H = np.kron(H,Hn)

   K = np.matmul(Jn2, H)                                   #строим матрицу T
   T = np.matmul(K, In2)
   R = np.matmul(T, Fz2)
   Z= R * U2[i] / R[0]
   Ap2 =np.add(Ap2, Z)
print("Итоговые апостериорные вероятности:")
print(Ap2)
















