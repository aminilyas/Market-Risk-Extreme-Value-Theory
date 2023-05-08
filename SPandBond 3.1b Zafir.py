# -*- coding: utf-8 -*-
"""
@author: Six
"""

#importing libraries 
import scipy.optimize as opt
import pandas as pd 
import numpy as np
import scipy.interpolate as inter
import math as mt


#importe file
data=pd.read_excel('SPandBondData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=data['SP500'].diff(periods=-1)+10*data['Bond10'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P

LP=LP.tail(1500)
print(LP) #print the L&P on the screen to chek and compare with Excel

#Compute the inverse of the empirical CDF, i.e. the quantile function
p = np.linspace(0,1,len(LP))                  
LossSorted = sorted(LP)
ppF = inter.interp1d(p,LossSorted)

#Compute the samples
N=10**3 #size of the samples
SampleU=np.random.uniform(0,1,size=N) #ff

SampleU=SampleU**(1/1500)

#Compute the distribution of the Maximum
SampleMax=ppF(SampleU)


def func(x):
    dumb=0
    for i in range(1, N+1):
        dumb=dumb+mt.log(x[1])+(x[2]+1)/x[2]*mt.log(1+x[2]*(SampleMax[i-1]-x[0])/x[1])+(1+x[2]*(SampleMax[i-1]-x[0])/x[1])**(-1/x[2])
    return dumb


muInf=np.nanmin(SampleU)
xInf=np.array([0,0,0])
xSup=np.array([np.inf,np.inf,0.35])

x0=[10,10,0.1]

bounds=opt.Bounds(lb=xInf, ub=xSup)

res=opt.minimize(func, x0, bounds=bounds)

muGEV=res.x[0]
sigGEV=res.x[1]
XsiGEV=res.x[2]

p90=0.9
q90=muGEV-sigGEV/XsiGEV*(1-(-mt.log(p90))**(-XsiGEV))
p95=0.95
q95=muGEV-sigGEV/XsiGEV*(1-(-mt.log(p95))**(-XsiGEV))
p99=0.99
q99=muGEV-sigGEV/XsiGEV*(1-(-mt.log(p99))**(-XsiGEV))