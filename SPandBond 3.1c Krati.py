# -*- coding: utf-8 -*-
"""
@author: Six
@edited by: Krati Sharma
"""

import pandas as pd 
import numpy as np
import scipy.interpolate as inter
import math as mt
import scipy.optimize as opt


data=pd.read_excel('SPandBondData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=2*data['SP500'].diff(periods=-1)+3*data['Bond10'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P

LP=LP.tail(1500)
print(LP) #print the L&P on the screen to chek and compare with Excel

#Compute the inverse of the empirical CDF, i.e. the quantile function
p = np.linspace(0,1,len(LP))                  
LossSorted = sorted(LP)
ppF = inter.interp1d(p,LossSorted)

n=len(LP)

#Compute the samples
N=10**3 #size of the samples
SampleU=np.random.uniform(0,1,size=N) 

SampleU=SampleU**(1/n)

#Compute the distribution of the Maximum
SampleMax=ppF(SampleU)

MaxSorted=sorted(SampleMax)

#size=len(LP)
mV = np.arange(1,N+1)

yData=np.log(-np.log(mV/(1+N)))

def func(x, mu, sig, xsi):

    return -1/xsi * np.log(1+xsi*(x-mu)/sig)

muInf=np.nanmin(SampleU)

xInf=np.array([0,0,0])

xSup=np.array([np.inf,np.inf,0.35])

popt,pcov = opt.curve_fit(func, MaxSorted, yData,bounds=(xInf, xSup))
perr = np.sqrt(np.diag(pcov))

#Computation of various quantile of the maximum of the loss
muGEV=popt[0]
sigGEV=popt[1]
Xsi=popt[2]

p90=0.9
q90=muGEV-sigGEV/Xsi*(1-(-mt.log(p90))**(-Xsi))
p95=0.95
q95=muGEV-sigGEV/Xsi*(1-(-mt.log(p95))**(-Xsi))
p99=0.99
q99=muGEV-sigGEV/Xsi*(1-(-mt.log(p99))**(-Xsi))

