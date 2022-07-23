import time
import numpy as np
import matplotlib.pylab as plt
from math import cos, pi, sqrt
from scipy.fft import dct


def my_dct2(f):
    '''
    Implementazione della DCT2.

    :param f: matrice dei valori puntuali
    :return c: matrice delle frequenze
    '''

    # Calcola il numero di righe (n) e colonne (m)
    n, m = np.shape(f) 

    # Copia f in c utilizzando valori float in 64 bit
    c = np.copy(f.astype('float64'))

    # Esegue la DCT1 sulle colonne
    for j in range(m):
        c[:,j] = my_dct1(c[:,j])

    # Esegue la DCT1 sulle righe
    for i in range(n):
        c[i,:] = my_dct1(c[i,:])

    return c


def my_dct1(f):
    '''
    Implementazione della DCT1.

    :param f: vettore dei valori puntuali
    :return c: vettore delle frequenze
    '''

    # Imposta i valori di f in formato float in 64 bit
    f = f.astype('float64')

    # Calcola il numero di elementi di f
    n = len(f)

    # Calcola la matrice di trasformazione
    D = compute_D(n)

    # Moltiplica la matrice di trasformazione e f
    c = np.dot(D, f)

    return c


def compute_D(n):
    '''
    Funzione per calcolare la matrice di trasformazione D.

    :param n: numero di elementi del vettore f per il calcolo della DCT1
    :return D: matrice di trasformazione
    '''

    # Calcola i valori alfa utilizzati per la matrice di trasformazione
    alpha_vect = np.zeros(n)
    alpha_vect[0] = 1.0 / sqrt(n)
    alpha_vect[1:n] = sqrt(2.0 / n)

    # Calcola la matrice di trasformazione
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i,j] = alpha_vect[i] * cos(pi * (2 * j + 1) * i / (2 * n))
    return D


def scipy_dct2(f):
    '''
    Implementazione della DCT2 tramite scipy.fft.
    '''
    return dct(dct(f.T, norm='ortho').T, norm='ortho')


def scipy_dct1(f):
    '''
    Implementazione della DCT1 tramite scipy.fft.
    '''
    return dct(f.T, norm='ortho')


def test():
    '''
    Funzione per verificare se le funzioni implementate per
    calcolare DCT1 e DCT2 rispettano i valori specificati
    nella consegna.
    '''

    # Array con i valori utilizzati per il test
    test_dct1 = np.array([231,  32, 233, 161,  24,  71, 140, 245])
    test_dct2 = np.array([[231,  32, 233, 161,  24,  71, 140, 245],
                        [247,  40, 248, 245, 124, 204,  36, 107],
                        [234, 202, 245, 167,   9, 217, 239, 173],
                        [193, 190, 100, 167,  43, 180,   8,  70],
                        [ 11,  24, 210, 177,  81, 243,   8, 112],
                        [ 97, 195, 203,  47, 125, 114, 165, 181],
                        [193,  70, 174, 167,  41,  30, 127, 245],
                        [ 87, 149,  57, 192,  65, 129, 178, 228]])

    # Stampa dei risultati. Il controllo della correttezza va svolto manualmente
    print("Verifica correttezza di scipy_dct1: ")
    result_scipy_test_dct1 = scipy_dct1(test_dct1)
    print(result_scipy_test_dct1)
    print()
    print("Verifica correttezza di my_dct1: ")
    result_my_test_dct1 = my_dct1(test_dct1)
    print(result_my_test_dct1)
    print()
    print("Verifica correttezza di scipy_dct2: ")
    result_scipy_test_dct2 = scipy_dct2(test_dct2)
    print(result_scipy_test_dct2)
    print()
    print("Verifica correttezza di my_dct2: ")
    result_my_test_dct2 = my_dct2(test_dct2)
    print(result_my_test_dct2)
    print()
 

def get_data():
    '''
    Funzione per calcolare i tempi di esecuzione delle implementazioni
    della DCT2.

    :return times_scipy_dct: tempi di esecuzione della DCT2 di scipy
    :return times_my_dct: tempi di esecuzione della DCT2 implementata in questo file
    :return matrix_dimensions: dimensioni utilizzate per creare matrici NxN
    :return n3: tempi di esecuzione di n^3
    :return n2_logn: tempi di esecuzione di n^2 * log(n)
    '''

    # Istanziazione degli array per contenere i valori dei tempi
    times_scipy_dct = []
    times_my_dct = []
    matrix_dimensions = []
    n3 = []
    n2_logn = []

    # Ripetizione dei calcoli dei tempi di esecuzione per più matrici
    # range(start, stop, step)
    for n in range(50, 901, 50): 
        print("Dimension: ", n)
        matrix_dimensions.append(n)

        # Creazione di una matrice random
        np.random.seed(5)
        matrix = np.random.uniform(low=0.0, high=255.0, size=(n, n))

        # Calcolo del tempo di esecuzione con scipy.fft
        time_start = time.perf_counter()
        result = scipy_dct2(matrix)
        time_end = time.perf_counter()
        times_scipy_dct.append(time_end - time_start)

        # Calcolo del tempo di esecuzione con la DCT2 implementata in questo file
        time_start = time.perf_counter()
        result = my_dct2(matrix)
        time_end = time.perf_counter()
        times_my_dct.append(time_end - time_start)

        # Calcolo del tempo di esecuzione con n^3
        n3.append(np.power(n, 3))

        # Calcolo del tempo di esecuzione con n^2 * log(n)
        n2_logn.append(np.power(n, 2) * np.log(n))

    return times_scipy_dct, times_my_dct, matrix_dimensions, n3, n2_logn


def plot(times_scipy_dct, times_my_dct, matrix_dimensions, n3, n2_logn):
    '''
    Funzione per stampare e plottare i tempi di esecuzione delle implementazioni
    della DCT2.

    :param times_scipy_dct: tempi di esecuzione della DCT2 di scipy
    :param times_my_dct: tempi di esecuzione della DCT2 implementata in questo file
    :param matrix_dimensions: dimensioni utilizzate per creare matrici NxN
    :param n3: tempi di esecuzione di n^3
    :param n2_logn: tempi di esecuzione di n^2 * log(n)
    '''    
    
    print("N used for matrix dimensions: ")
    for i in range(len(matrix_dimensions)):
        print(str(matrix_dimensions[i]), end = " ")
    print()

    print("Execution times with scipy DCT2: ")
    for i in range(len(times_scipy_dct)):
        print(str(times_scipy_dct[i]), end = " ")
    print()

    print("Execution times with my DCT2: ")
    for i in range(len(times_my_dct)):
        print(str(times_my_dct[i]), end = " ")
    print()

    print("Execution times with N^2 * log(N): ")
    for i in range(len(n2_logn)):
        print(str(n2_logn[i]), end = " ")
    print()

    print("Execution times with N^3: ")
    for i in range(len(n3)):
        print(str(n3[i]), end = " ")
    print()

    print("Proportions for scipy DCT2")
    for i in range(len(times_scipy_dct)):
        print(str(n2_logn[i] / times_scipy_dct[i]), end = " ")
    print()

    print("Proportions for my DCT2")
    for i in range(len(times_my_dct)):
        print(str(n3[i] / times_my_dct[i]), end = " ")
    print()

    new_n2_logn = [x / 100000000 for x in n2_logn]

    new_n3 = [x / 500000 for x in n3]
    
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(matrix_dimensions, times_scipy_dct,  c='r', label='scipy DCT2', linewidth=1.0)
    ax.plot(matrix_dimensions, times_my_dct, c='b', label='my DCT2', linewidth=1.0)
    legend = plt.legend()
    plt.xlabel("Dimension N for NxN matrix")
    plt.ylabel("Time (s)")
    plt.show()
    fig.savefig("NormalPlot.png", dpi=fig.dpi)

    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(matrix_dimensions, times_scipy_dct,  c='r', label='scipy DCT2', linewidth=1.0)
    ax.plot(matrix_dimensions, times_my_dct, c='b', label='my DCT2', linewidth=1.0)
    ax.plot(matrix_dimensions, n2_logn,  c='r', label='(N^2)*log(N)', linewidth=1.0, linestyle="dotted")
    ax.plot(matrix_dimensions, n3, c='b', label='N^3', linewidth=1.0, linestyle="dotted")
    legend = plt.legend()
    plt.xlabel("Dimension N for NxN matrix")
    plt.ylabel("Time (s)")
    plt.show()
    fig.savefig("NormalPlotWithProportions.png", dpi=fig.dpi)

    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(matrix_dimensions, times_scipy_dct,  c='r', label='scipy DCT2', linewidth=1.0)
    ax.plot(matrix_dimensions, times_my_dct, c='b', label='my DCT2', linewidth=1.0)
    ax.plot(matrix_dimensions, new_n2_logn,  c='r', label='(N^2)*log(N) / (10^8)', linewidth=1.0, linestyle="dotted")
    ax.plot(matrix_dimensions, new_n3, c='b', label='(N^3) / (5*10^5)', linewidth=1.0, linestyle="dotted")
    legend = plt.legend()
    plt.xlabel("Dimension N for NxN matrix")
    plt.ylabel("Time (s)")
    plt.show()
    fig.savefig("ModifiedPlot.png", dpi=fig.dpi)


def main():
    test()
    times_scipy_dct, times_my_dct, matrix_dimensions, n3, n2_logn = get_data()
    plot(times_scipy_dct, times_my_dct, matrix_dimensions, n3, n2_logn)


if __name__ == '__main__':
    main()
    






