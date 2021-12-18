#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
import timeit
import threading

# Recebe um valor de S e carrega duas matrizes na saída
def FileToMatrix(s):

    string = './data/A'+str(s)+'x'+str(s)+'.txt'
    string2= './data/B'+str(s)+'x'+str(s)+'.txt'

    arquivoA = open(string, 'r')
    arquivoB = open(string2, 'r')

    a = [[x for x in line.split()] for line in arquivoA.readlines()]
    b = [[x for x in line.split()] for line in arquivoB.readlines()]

    a = [i for i in a if i!='\n' or i!=str(s)+'\n']
    a = a[1::]    
    b = [i for i in b if i!='\n' or i!=str(s)+'\n']
    b = b[1::] 

    data = np.array(a)
    datab = np.array(b)
    data = data.reshape((s,s))
    datab = datab.reshape((s,s))

    return data.astype(int), datab.astype(int)



# def MultiplicaMatrizes(a,b):
#     c = [[0 for x in range(len(a))] for y in range(len(b[0]))]    
#     for i in range(len(a)):
#         for j in range(len(b[0])):
#             for k in range(len(b)):
#                 c[i][j] += a[i][k] * b[k][j]
#     return c

def MultiplicaMatrizes (matrizA, matrizB):
    threads = []
    result=[]
    for i in range(len(matrizA)):
        linha = matrizA[i]
        resultLinha=[]
        for j in range(len(matrizB)):
            coluna =[]
            for k in range (len(matrizB)):
                coluna.append(matrizB[k][j])
            MultiplicaVetores(linha, coluna, resultLinha)

        result.append(resultLinha)
    
    return np.array(result) 

def MultiplicaVetores (a,b, resultLinha):
    soma = 0
    for i in range (len(a)):
        soma+=(a[i]*b[i])

    resultLinha.append(soma)


def concorrente (matrizA, matrizB):
    threads = []
    result=[]
    for i in range(len(matrizA)):
        linha = matrizA[i]
        resultLinha=[]
        for j in range(len(matrizB)):
            coluna =[]
            for k in range (len(matrizB)):
                coluna.append(matrizB[k][j])

            x = threading.Thread(target = MultiplicaVetores, args=(linha, coluna, resultLinha))
            x.start()
            threads.append(x)

        result.append(resultLinha)

    for thread in threads:
        thread.join()
    
    return np.array(result)


#for i in range(len(matrizA)):
    #print(matrizA[0][i])
#print("--------------------------------")
#for i in range(len(matrizB[0])):
    #print(matrizB[i][0])
lista_tempos = []
print("SEQUENCIAL")
# for i in [4,8,16,32,64,128, 256, 512, 1024, 2048]:
# for i in [4,8,16,32,64,128, 256, 512]:
for i in [4, 8]:
    matrizA, matrizB  =  FileToMatrix(i)
    start_time = time.time()
    print(np.array(MultiplicaMatrizes(matrizA,matrizB)))
    np.array(MultiplicaMatrizes(matrizA,matrizB))
    end_time = time.time()
    lista_tempos.append(end_time-start_time)

print(lista_tempos)
lista_tempos = []
print("CONCORRÊNCIA")
# for i in [4,8,16,32,64,128, 256, 512]:
for i in [4, 8]:
    matrizA, matrizB  =  FileToMatrix(i)
    start_time = time.time()
    print(np.array(concorrente(matrizA,matrizB)))
    np.array(concorrente(matrizA,matrizB))
    end_time = time.time()
    lista_tempos.append(end_time-start_time)

print(lista_tempos)

  
#np.set_printoptions(threshold=np.inf)


#print(end_time-start_time)