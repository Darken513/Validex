import numpy as np
from scipy import stats

def calculateSlopePerSeries100(xy, refIdx):
    xy100 = xy[refIdx]
    slopes = []
    for testIndx in range(len(xy100)):
        x100 = xy100[testIndx][0]
        y100 = xy100[testIndx][1]
        slopes.append(y100/x100)
    return slopes

def calculateSlopePerSeries_CD(xy):
    n = len(xy)
    m = len(xy[0])
    data = {'slopes':[], 'intercepts':[]}
    for testIndx in range(m):
        x = []
        y = []
        for serieIdx in range(n):
            x.append(xy[serieIdx][testIndx][0])
            y.append(xy[serieIdx][testIndx][1])
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        data['slopes'].append(slope)
        data['intercepts'].append(intercept)
    return data 