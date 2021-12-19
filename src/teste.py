import numpy as np
from numpy.testing import assert_array_equal
import threading
from time import time

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

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (nrows, ncols, n, m) where
    n * nrows, m * ncols = arr.shape.
    This should be a view of the original array.
    """
    h, w = arr.shape
    n, m = h // nrows, w // ncols
    return arr.reshape(nrows, n, ncols, m).swapaxes(1, 2)


def do_dot(a, b, out):
    #np.dot(a, b, out)  # does not work. maybe because out is not C-contiguous?
    out[:] = MultiplicaMatrizes(a, b)  # less efficient because the output is stored in a temporary array?

def insert_at_pos( lst, pos, val, default=None ):

    if( len(lst) > pos ):
       lst.insert( pos, val )
    else:
        for _ in range( pos - len(lst) ):
            lst.append( default )
        lst.append( val )

    return lst

def MultiplicaMatrizes (matrizA, matrizB):
    result = []
    for i in range(len(matrizA)):
        linha = matrizA[i]
        resultLinha=[]
        for j in range(len(matrizB)):
            coluna =[]
            for k in range (len(matrizB)):
                coluna.append(matrizB[k][j])
            MultiplicaVetores(linha, coluna, resultLinha)

        insert_at_pos(result, i, np.array(resultLinha))
    return result

def MultiplicaVetores (a,b, resultLinha):
    soma = 0
    for i in range (len(a)):
        soma+=(a[i]*b[i])

    resultLinha.append(soma)

def pardot(a, b, nblocks):
    """
    Return the matrix product a * b.
    The product is split into nblocks * nblocks partitions that are performed
    in parallel threads.
    """
    # n_jobs = nblocks * nblocks
    # print('running {} jobs in parallel'.format(n_jobs))

    out = np.empty((a.shape[0], b.shape[1]), dtype=a.dtype)

    out_blocks = blockshaped(out, 2, 4)
    a_blocks = blockshaped(a, 2, 1)
    b_blocks = blockshaped(b, 1, 4)
    print(a.shape)
    print(b.shape)


    threads = []
    for i in range(nblocks):
        for j in range(nblocks):
            th = threading.Thread(target=do_dot, 
                                  args=(a_blocks[i, 0, :, :], 
                                        b_blocks[0, j, :, :], 
                                        out_blocks[i, j, :, :]))
            th.start()
            threads.append(th)

    for th in threads:
        th.join()

    return out


if __name__ == '__main__':
    for i in [4]:
        matrizA, matrizB  =  FileToMatrix(i)
        print(matrizA, '\n')
        print(matrizB)
        # a = np.ones((4, 3), dtype=int)
        # b = np.arange(18, dtype=int).reshape(3, 6)
        # assert_array_equal(pardot(matrizA, matrizB, 2, 2), np.dot(matrizA, matrizB))

        a = np.random.randn(1500, 1500).astype(int)

        start = time()
        print(pardot(matrizA, matrizB, 2))
        time_par = time() - start
        print('pardot: {:.10f} seconds taken'.format(time_par))

        start = time()
        print(np.dot(matrizA, matrizB))
        time_dot = time() - start
        print('np.dot: {:.10f} seconds taken'.format(time_dot))