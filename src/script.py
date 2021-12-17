import numpy as np

# Recebe um valor de S e carrega duas matrizes na saída
def FileToMatrix(s):

    string = './data/A'+str(s)+'x'+str(s)+'.txt'
    string2= './data/B'+str(s)+'x'+str(s)+'.txt'

    arquivoA = open(string, 'r')
    arquivoB = open(string2, 'r')

    a = [[x for x in line.split()] for line in arquivoA.readlines()]
    b = [[x for x in line.split()] for line in arquivoB.readlines()]

    for i in a:
        if i=='\n' or i==str(s)+'\n':
            a.remove(i)
    a = a[1::]    

    for i in b:
        if i=='\n' or i==str(s)+'\n':
            b.remove(i)
    b = b[1::] 

    data = np.array(a)
    datab = np.array(b)
    data = data.reshape((s,s))
    datab = datab.reshape((s,s))

    return data.astype(int), datab.astype(int)

def MultiplicaMatrizes(a,b):
    c = [[0 for x in range(len(a))] for y in range(len(b[0]))]    
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                c[i][j] += a[i][k] * b[k][j]
    return c 


  

matrizA, matrizB  =  FileToMatrix(4)
# :D
#print(np.matmul(matrizA,matrizB))
print(np.array(MultiplicaMatrizes(matrizA,matrizB)))