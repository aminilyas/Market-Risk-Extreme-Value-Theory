# -*- coding: utf-8 -*-
"""
@author: Six
@edited by: Amin Ilyas

"""

#importing libraries 
import scipy.special as spa
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

n=len(LP)

#Compute the inverse of the empirical CDF, i.e. the quantile function
p = np.linspace(0,1,len(LP))                  
LossSorted = sorted(LP)
ppF = inter.interp1d(p,LossSorted)

#Compute the samples
N=10**3 #size of the samples
SampleU=np.random.uniform(0,1,size=N) #ff

SampleU=SampleU**(1/n)

#Compute the distribution of the VaR
SampleLoss=ppF(SampleU)
SampleLoss2=SampleLoss**2

mu1=SampleLoss.mean()
mu2=SampleLoss2.mean()

sig2=mu2-mu1**2

#Computation of the coefficients
Xsi=0.35
A1=(spa.gamma(1-Xsi)-1)/Xsi
A2=(spa.gamma(1-2*Xsi)-spa.gamma(1-Xsi)**2)/Xsi**2
sig2GEV=sig2/A2
sigGEV=sig2GEV**0.5
muGEV=mu1-sigGEV*A1

#Computation of various quantile of the maximum of the loss
p90=0.9
q90=muGEV-sigGEV/Xsi*(1-(-mt.log(p90))**(-Xsi))
p95=0.95
q95=muGEV-sigGEV/Xsi*(1-(-mt.log(p95))**(-Xsi))
p99=0.99
q99=muGEV-sigGEV/Xsi*(1-(-mt.log(p99))**(-Xsi))