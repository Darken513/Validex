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

def calculate_variance(data):
    n = len(data)
    if n == 0:
        raise ValueError("Array must not be empty")
    mean = sum(data) / n
    squared_diff = [(x - mean) ** 2 for x in data]
    variance = sum(squared_diff) / n
    return variance

def slope_variance(x, Xbars, Yij_flatten):
    VarYij = calculate_variance(Yij_flatten)
    dev = 0
    for i in range(len(x)):
        for j in range(len(x[i])):
            dev += (x[i][j] - Xbars[i])**2
    return VarYij / dev

def calculate_TestT_pente(b1, b2, r1, r2, x1, x2, y1, y2):
    n1 = len(x1)*len(x1[0])
    SCE1X = math.calculateSCEXFlat(n1, x1)
    
    n2 = len(x2)*len(x2[0])
    SCE2X = math.calculateSCEXFlat(n2, x2)
    
    SCE1Y = math.calculateSCEYFlat(n1, y1)
    SCE2Y = math.calculateSCEYFlat(n2, y2)
    
    SCE1r = math.calculateSCER(r1, SCE1Y)
    SCE2r = math.calculateSCER(r2, SCE2Y)
    
    S2C = math.calculateS2C(n1, n2, SCE1r, SCE2r)
    
    return abs(b1-b2)/pyMath.sqrt(S2C* (1/SCE1X + 1/SCE2X))

def calculate_TestT_ord(a1, a2, r1, r2, x1, x2, y1, y2):
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
    
    return abs(a1-a2)/pyMath.sqrt(S2C* (1/n1 + x1mean**2/SCE1X + 1/n2 + x2mean**2/SCE2X))

def calculate_TestT_ord0(a1, r1, x1, y1):
    n1 = len(x1)*len(x1[0])
    x1mean = sum(x1.flatten())/len(x1.flatten())
    
    SCE1X = math.calculateSCEXFlat(n1, x1)
    SCE1Y = math.calculateSCEYFlat(n1, y1)
    SCE1r = math.calculateSCER(r1, SCE1Y)
    
    S2C = SCE1r / (n1 - 2)
    
    return abs(a1)/pyMath.sqrt(S2C* (1/n1 + x1mean**2/SCE1X))


def calculate_TestTold(n, m, b1, b2, x1, y1, x2, y2):
    Xbars1 = math.calculateXbars(n, m, x1)
    Yij1_flatten = math.calculateYij(n, m, b1, x1, y1, Xbars1).flatten()

    Xbars2 = math.calculateXbars(n, m, x2)
    Yij2_flatten = math.calculateYij(n, m, b2, x2, y2, Xbars2).flatten()

    Vslope1 = slope_variance(x1, Xbars1, Yij1_flatten)
    Vslope2 = slope_variance(x2, Xbars2, Yij2_flatten)
    
    return abs(b1 - b2)/pyMath.sqrt(Vslope1+Vslope2)
#------------------------------------------------------------------------------------------------#
#---------------------------------- Implementing Student test -----------------------------------#
#------------------------------------------------------------------------------------------------#

n = 5
m = 3
b1 = 798.528273
a1 = -1345.52
corelation1 = 0.9998
b2 = 791.593
a2 = -1113.5
corelation2 = 0.9998

x1 = np.array([[0.0]*m]*n)
y1 = np.array([[0.0]*m]*n)
x2 = np.array([[0.0]*m]*n)
y2 = np.array([[0.0]*m]*n)

xy1 = [
    [[96.5, 76626.0], [96.8, 75154.0], [96.7, 76049.0]], 
    [[130.0, 103197.0], [129.8, 101786.0], [129.7, 101858.0]], 
    [[161.8, 128105.0], [161.5, 126865.0], [161.2, 127788.0]], 
    [[195.5, 155967.0], [195.3, 153848.0], [195.3, 153608.0]], 
    [[227.8, 181879.0], [228.6, 180355.0], [228.2, 180909.0]]
]

xy2 = [
    [[97.2, 76521.0], [97, 75251.0], [96.8, 75297.0]], 
    [[130.5, 102749.0], [131.2, 102210.0], [131.0, 102283.0]], 
    [[161.1, 126779.0], [163, 127242.0], [161.2, 126801.0]], 
    [[194.1, 153035.0], [194.1, 151598.0], [194.5, 153867.0]], 
    [[226.4, 170584.0], [225.6, 176002.0], [225.9, 178332.0]]
]

for j in range(n):
    for i in range(m):
        x1[j][i] = xy1[j][i][0] 
        y1[j][i] = xy1[j][i][1] 
        
for j in range(n):
    for i in range(m):
        x2[j][i] = xy2[j][i][0] 
        y2[j][i] = xy2[j][i][1] 
       
Xbars1 = math.calculateXbars(n, m, x1)
Yij1_flatten = math.calculateYij(n, m, b1, x1, y1, Xbars1).flatten()

Xbars2 = math.calculateXbars(n, m, x2)
Yij2_flatten = math.calculateYij(n, m, b2, x2, y2, Xbars2).flatten()

Vslope1 = slope_variance(x1, Xbars1, Yij1_flatten)
Vslope2 = slope_variance(x2, Xbars2, Yij2_flatten)

T_pente = calculate_TestT_pente(b1, b2, corelation1, corelation2, x1, x2, y1, y2)
print(T_pente)
T_ord = calculate_TestT_ord(a1, a2, corelation1, corelation2, x1, x2, y1, y2)
print(T_ord)

print(calculate_TestT_ord0(a2, corelation2, x2, y2))