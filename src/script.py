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

    return data.astype(np.float32), datab.astype(np.float32)


def MultiplicaMatrizes (a, b):
    c = [[0 for x in range(len(a))] for y in range(len(b[0]))]    
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                c[i][j] += a[i][k] * b[k][j]
    return c 

def blocoModelado(arr, nrows, ncols):
    h, w = arr.shape
    n, m = h // nrows, w // ncols
    return arr.reshape(nrows, n, ncols, m).swapaxes(1, 2)

def do_dot(a, b, result):
    result[::] = np.array(MultiplicaMatrizes(a, b))

def concorrente (a, b, tamanho):
    result = np.empty((a.shape[0], b.shape[1]), dtype=a.dtype)
    num1 = 2
    num2 = 2
    if(len(a)>32):
        num1=4
        num2=8
    elif(len(a)>128):
        num1=8
        num2=16
    elif(len(a)>512):
        num1=16
        num2=32
    result_bloco = blocoModelado(result, num2, num2)
    a_bloco = blocoModelado(a, num2, 1)
    b_bloco = blocoModelado(b, 1, num2)

    threads = []
    
    for i in range(num1):
        for j in range(num2):
            x = threading.Thread(target = do_dot, args=(a_bloco[i, 0, :, :], b_bloco[0, j, :, :], result_bloco[i, j, :, :]))
            x.start()
            threads.append(x)

    for thread in threads:
        thread.join()
    
    return result

lista_tempos = []
print("SEQUENCIAL")
# for i in [4,8,16,32,64,128, 256, 512, 1024, 2048]:
for i in [4,8,16,32,64,128, 256, 512]:
    matrizA, matrizB  =  FileToMatrix(i)
    start_time = time.time()
    np.array(MultiplicaMatrizes(matrizA,matrizB))
    end_time = time.time()
    lista_tempos.append(end_time-start_time)

print(lista_tempos)
lista_tempos = []
print("CONCORRÊNCIA")
for i in [1024]:
    matrizA, matrizB  =  FileToMatrix(i)
    start_time = time.time()
    concorrente(matrizA,matrizB, i)
    end_time = time.time()
    lista_tempos.append(end_time-start_time)

print(lista_tempos)
