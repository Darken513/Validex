import numpy as np
import math as pyMath
import mathUtils as math
from scipy.stats import t

#------------------------------------------------------------------------------------------------#
#------------------------------- Util functions for Student test --------------------------------#
#------------------------------------------------------------------------------------------------#
def tStudentCV(alpha, df): 
    critical_value = t.ppf(1 - alpha/2, df)
    return round(critical_value,3)

def __calculate_variance(data):
    n = len(data)
    if n == 0:
        raise ValueError("Array must not be empty")
    mean = sum(data) / n
    squared_diff = [(x - mean) ** 2 for x in data]
    variance = sum(squared_diff) / n
    return variance

def __slope_variance(x, Xbars, Yij_flatten):
    VarYij = __calculate_variance(Yij_flatten)
    dev = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
            dev += (x[i][j] - Xbars[i])**2
    return VarYij / dev

def calculate_TestT_pente(b1, b2, r1, r2, xy1, xy2):
    n = len(xy1)
    m = len(xy1[0])
    
    x1 = np.array([[0.0]*m]*n)
    y1 = np.array([[0.0]*m]*n)
    x2 = np.array([[0.0]*m]*n)
    y2 = np.array([[0.0]*m]*n)
    
    for j in range(n):
        for i in range(m):
            x1[j][i] = xy1[j][i][0] 
            y1[j][i] = xy1[j][i][1] 
            
    for j in range(n):
        for i in range(m):
            x2[j][i] = xy2[j][i][0] 
            y2[j][i] = xy2[j][i][1] 

    n1 = len(x1)*len(x1[0])
    SCE1X = math.calculateSCEXFlat(n1, x1)
    
    n2 = len(x2)*len(x2[0])
    SCE2X = math.calculateSCEXFlat(n2, x2)
    
    SCE1Y = math.calculateSCEYFlat(n1, y1)
    SCE2Y = math.calculateSCEYFlat(n2, y2)
    
    SCE1r = math.calculateSCER(r1, SCE1Y)
    SCE2r = math.calculateSCER(r2, SCE2Y)
    
    S2C = math.calculateS2C(n1, n2, SCE1r, SCE2r)
    
    return round(abs(b1-b2)/pyMath.sqrt(S2C* (1/SCE1X + 1/SCE2X)), 2)

def calculate_TestT_ord(a1, a2, r1, r2, xy1, xy2):
    n = len(xy1)
    m = len(xy1[0])
    
    x1 = np.array([[0.0]*m]*n)
    y1 = np.array([[0.0]*m]*n)
    x2 = np.array([[0.0]*m]*n)
    y2 = np.array([[0.0]*m]*n)
    
    for j in range(n):
        for i in range(m):
            x1[j][i] = xy1[j][i][0] 
            y1[j][i] = xy1[j][i][1] 
            
    for j in range(n):
        for i in range(m):
            x2[j][i] = xy2[j][i][0] 
            y2[j][i] = xy2[j][i][1] 
            
    n1 = len(x1)*len(x1[0])
    x1mean = sum(x1.flatten())/len(x1.flatten())
    SCE1X = math.calculateSCEXFlat(n1, x1)
    
    n2 = len(x2)*len(x2[0])
    SCE2X = math.calculateSCEXFlat(n2, x2)
    x2mean = sum(x2.flatten())/len(x2.flatten())
    
    SCE1Y = math.calculateSCEYFlat(n1, y1)
    SCE2Y = math.calculateSCEYFlat(n2, y2)
    
    SCE1r = math.calculateSCER(r1, SCE1Y)
    SCE2r = math.calculateSCER(r2, SCE2Y)
    
    S2C = math.calculateS2C(n1, n2, SCE1r, SCE2r)
    
    return round(abs(a1-a2)/pyMath.sqrt(S2C* (1/n1 + x1mean**2/SCE1X + 1/n2 + x2mean**2/SCE2X)), 2)

def calculate_TestT_ord0(a, r, xy):
    n = len(xy)
    m = len(xy[0])
    
    x = np.array([[0.0]*m]*n)
    y = np.array([[0.0]*m]*n)
    
    for j in range(n):
        for i in range(m):
            x[j][i] = xy[j][i][0] 
            y[j][i] = xy[j][i][1] 
            
    N = len(x)*len(x[0])
    
    xmean = sum(x.flatten())/len(x.flatten())
    
    SCEX = math.calculateSCEXFlat(N, x)
    SCEY = math.calculateSCEYFlat(N, y)
    SCEr = math.calculateSCER(r, SCEY)
    
    S2C = SCEr / (N - 2)
    
    return round(abs(a)/pyMath.sqrt(S2C* (1/n + xmean**2/SCEX)), 2)


def __calculate_TestTold(n, m, b1, b2, x1, y1, x2, y2):
    Xbars1 = math.calculateXbars(n, m, x1)
    Yij1_flatten = math.calculateYij(n, m, b1, x1, y1, Xbars1).flatten()

    Xbars2 = math.calculateXbars(n, m, x2)
    Yij2_flatten = math.calculateYij(n, m, b2, x2, y2, Xbars2).flatten()

    Vslope1 = __slope_variance(x1, Xbars1, Yij1_flatten)
    Vslope2 = __slope_variance(x2, Xbars2, Yij2_flatten)
    
    return round(abs(b1 - b2)/pyMath.sqrt(Vslope1+Vslope2), 2)