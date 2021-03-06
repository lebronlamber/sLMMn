__author__ = 'Haohan Wang'

import scipy
# from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans

from utility.simpleFunctions import *

epsilon = 1e-8

def generateData(seed, test=False):
    plt = None
    if test:
        from matplotlib import pyplot as plt
    np.random.seed(seed)

    dense = 0.01

    n = 100
    p1 = 1000
    p2 = 10
    g = 5
    sig = 1
    sigC = 1
    p = p1

    we = 0.

    center1 = np.random.normal(0, 1, [g, p1])
    center2 = np.random.normal(0, 1, [g, p2])
    sample = n / g
    X = []
    Z = []

    for i in range(g):
        x = np.random.multivariate_normal(center1[i, :], sig * np.diag(np.ones([p1, ])), size=sample)
        X.extend(x)
        for j in range(sample):
            Z.append(center2[i,:])
    X = np.array(X)

    # for i in range(g):
    #     z = np.random.multivariate_normal(center2[i, :], sig * np.diag(np.ones([p2, ])), size=sample)
    #     Z.extend(z)
    Z = np.array(Z)



    X[X > -1] = 1
    X[X <= -1] = 0
    # Z[Z > -1] = 1
    # Z[Z <= -1] = 0

    if test:
        plt.imshow(X)
        plt.show()

    featureNum = int(p * dense)
    idx = scipy.random.randint(0, p, featureNum).astype(int)
    idx = sorted(idx)
    w = 1 * np.random.normal(0, 1, size=featureNum)
    ypheno = scipy.dot(X[:, idx], w)
    ypheno = (ypheno - ypheno.mean()) / ypheno.std()
    ypheno = ypheno.reshape(ypheno.shape[0])
    error = np.random.normal(0, 1, n)

    C = np.dot(Z, Z.T)
    C1 = C
    if test:
        plt.imshow(C1)
        plt.show()
        print C1

    S, K = np.linalg.eigh(C)
    S[S<epsilon] = 0
    if test:
        ind = np.array(xrange(S.shape[0]))
        plt.scatter(ind[:-1], mapping2ZeroOne(S[:-1]), color='y', marker='+')
        print S
        plt.scatter(ind[:-1], mapping2ZeroOne(np.power(S, 2)[:-1]), color='b', marker='+')
        print np.power(S, 2)
        plt.scatter(ind[:-1], mapping2ZeroOne(np.power(S, 4)[:-1]), color='m', marker='+')
        print np.power(S, 4)
        plt.show()
    if not test:
        np.savetxt('../toyData/Kva.csv', S, delimiter=',')
        np.savetxt('../toyData/Kve.csv', K, delimiter=',')
        np.savetxt('../toyData/X.csv', X, delimiter=',')
    causal = np.array(zip(idx, w))
    if not test:
        np.savetxt('../toyData/causal.csv', causal, '%5.2f', delimiter=',')

    y = we * error + ypheno
    if not test:
        np.savetxt('../toyData/K0/y.csv', y, '%5.2f', delimiter=',')
    yK1 = np.random.multivariate_normal(ypheno, sigC * C1, size=1)
    yK1 = yK1.reshape(yK1.shape[1])
    yK1 = we * error + yK1
    if not test:
        np.savetxt('../toyData/K1/y.csv', yK1, '%5.2f', delimiter=',')

    C2 = np.dot(C, C)
    yK2 = np.random.multivariate_normal(ypheno, sigC * C2, size=1)
    yK2 = yK2.reshape(yK2.shape[1])
    yK2 = we * error + yK2
    if test:
        plt.imshow(C2)
        plt.show()
        print C2
    if not test:
        np.savetxt('../toyData/K2/y.csv', yK2, '%5.2f', delimiter=',')

    C3 = np.dot(np.dot(C, C),np.dot(C, C))
    yKn = np.random.multivariate_normal(ypheno, sigC * C3, size=1)
    yKn = yKn.reshape(yKn.shape[1])
    yKn = we * error + yKn
    if test:
        plt.imshow(C3)
        plt.show()
        print C3
    if not test:
        np.savetxt('../toyData/Kn/y.csv', yKn, '%5.2f', delimiter=',')

    if test:
        x = xrange(len(y))
        plt.scatter(x, y, color='g')
        plt.scatter(x, yK1, color='y')
        plt.scatter(x, yK2, color='b')
        plt.scatter(x, yKn, color='m')
        plt.show()

        def imshowY(y):
            y = y.reshape(y.shape[0], 1)
            plt.imshow(np.dot(y, y.T))
            plt.show()

        imshowY(y)
        imshowY(yK1)
        imshowY(yK2)
        imshowY(yKn)

        np.savetxt('tmp_c2.csv', C2, delimiter=',')
        np.savetxt('tmp_c3.csv', C3, delimiter=',')


if __name__ == '__main__':
    generateData(2, test=True)
