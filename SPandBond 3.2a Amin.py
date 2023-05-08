# -*- coding: utf-8 -*-
"""
@author: Six
@edited by: Amin Ilyas
"""

#importing libraries 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

#importe file
data=pd.read_excel('SPandBondData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=data['SP500'].diff(periods=-1)+10*data['Bond10'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P


def meanExcessFunc(u):
    num=LP-u
    num=num[num>0]
    den=len(num)
    num=np.sum(num)
    return num/den

N =1000

u=np.linspace(0,40,N)

meanExcessVec=np.zeros(N)

for i in range(0, N):
    meanExcessVec[i]=meanExcessFunc(u[i])
#v=meanExcess(u)

plt.scatter(u,meanExcessVec)

uThreshold1=25
uThreshold2=35
u=u[u>uThreshold1]
u=u[u<uThreshold2]
N=len(u)
meanExcessVec=np.zeros(N)

for i in range(0, N):
    meanExcessVec[i]=meanExcessFunc(u[i])


u = sm.add_constant(u)
reg=sm.OLS(meanExcessVec,u)
res = reg.fit()
param=res.params
xsi=param[1]/(1+param[1])
beta=param[0]*(1-xsi)

n=len(LP)
nu=len(LP[LP>uThreshold2])

alpha=0.95
alphaVaR= uThreshold2+beta/xsi*((n/nu*(1-alpha))**(-xsi)-1)

