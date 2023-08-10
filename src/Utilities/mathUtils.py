import numpy as np

def calculateXbars(n,m,x_coords):
    Xbars = np.array([0.0]*n)
    for j in range(n):
        Xbars[j] = sum(x_coords[j])/m
    return Xbars

def calculateYij(n, m, b, x_coords, y_coords, Xbars):
    Yij = np.array([[0.0]*m]*n)
    for j in range(n):
        for i in range(m):
            Yij[j][i] = round(y_coords[j][i] + b*(Xbars[j] - x_coords[j][i]))
    return Yij

def calculateVarianceY(m, y_coords):
    mean_y = sum(y_coords) / m
    variance = sum((y - mean_y)**2 for y in y_coords) / (m-1)
    return round(variance)

def calculateS2j(n, m, y_coords):
    S2j = np.array([0.0]*n)
    for j in range(n):
        S2j[j] = calculateVarianceY(m, y_coords[j])
    return S2j

def calculateSCEX(n, m, X, Xbars):
    toret = 0
    for i in range(n):
        for j in range(m):
            toret = (X[i][j] - Xbars[i])**2
    return toret

def calculateSCEY(n, m, Y, Ybars):
    toret = 0
    for i in range(n):
        for j in range(m):
            toret = (Y[i][j] - Ybars[i])**2
    return toret


def calculateSCEXFlat(n, X):
    toret = 0
    xFlat = X.flatten()
    Xbar = sum(xFlat)/len(xFlat)
    for i in range(n):
        toret = (xFlat[i] - Xbar)**2
    return toret

def calculateSCEYFlat(n, Y):
    toret = 0
    yFlat = Y.flatten()
    Ybar = sum(yFlat)/len(yFlat)
    for i in range(n):
        toret = (yFlat[i] - Ybar)**2
    return toret

def calculateSCER(r, SCEY):
    return (1 - r**2) * SCEY

def calculateS2C(n1, n2, SCE1r, SCE2r):
    return (SCE1r+SCE2r) / (n1 + n2 -4)