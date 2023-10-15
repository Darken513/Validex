import numpy as np
import mathUtils as math
from scipy.stats import f

#------------------------------------------------------------------------------------------------#
#------------------------------- Util functions for Fisher test ---------------------------------#
#------------------------------------------------------------------------------------------------#

def fisherCVTable(alpha, df, dfn):
    return round(f.ppf(1-alpha, df, dfn),2)

def calculate_VTotal(n, m, Yij):
    Y = sum(sum(Yij))/(n*m)
    toret = 0
    for j in range(n):
        for i in range(m):
            toret += (Yij[j][i] - Y)**2
    return toret   

def calculate_VTotalExactitude(n, m, slope, intercept, XY):
    toret = 0
    for j in range(n):
        for i in range(m):
            toret += (XY[j][i][1] - (intercept + slope*XY[j][i][0]))**2
    return toret

def calculate_Vregression(n, m, b, Xbars):
    X = sum(Xbars)/n
    toret = 0
    for j in range(n):
        toret += m*(Xbars[j] - X)**2
    return toret * b**2
 
def calculate_Vresiduel(n, m, VT, VR):
    VR2 = VT - VR
    return VR2/(n*m - 2)
     
def calculate_VerreurExp(n, m, Yij):
    toret = 0
    for j in range(n):
        Ybar = sum(Yij[j])/len(Yij[j])
        for i in range(m):
            toret += (Yij[j][i] - Ybar)**2
    return toret/(n*m - n)

def calculate_VerreurReg(n, m, VT, VR, VEE):
    SR2 = VT - VR
    return (SR2 - VEE*(n*m - n))/(n-2)

def calculateFisherHS(n, m, b, xy):
    x = np.array([[0.0]*m]*n)
    y = np.array([[0.0]*m]*n)
    for j in range(n):
        for i in range(m):
            x[j][i] = xy[j][i][0] 
            y[j][i] = xy[j][i][1] 
    Xbars = math.calculateXbars(n, m, x)
    Yij = math.calculateYij(n, m, b, x, y, Xbars)
    VT = calculate_VTotal(n, m, Yij)
    VR = calculate_Vregression(n, m, b, Xbars)
    VR2 = calculate_Vresiduel(n, m, VT, VR)
    return round(VR/VR2, 2)

def calculateFisherNS(n, m, b, xy):
    x = np.array([[0.0]*m]*n)
    y = np.array([[0.0]*m]*n)
    for j in range(n):
        for i in range(m):
            x[j][i] = xy[j][i][0] 
            y[j][i] = xy[j][i][1] 
    Xbars = math.calculateXbars(n, m, x)
    Yij = math.calculateYij(n, m, b, x, y, Xbars)
    VT = calculate_VTotal(n, m, Yij)
    VR = calculate_Vregression(n, m, b, Xbars)
    VEE = calculate_VerreurExp(n, m, Yij)
    VER = calculate_VerreurReg(n, m, VT, VR, VEE)
    return round(VER/VEE, 2)