# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:43:58 2022

@author: Esteban Lopez
"""

#Distribution of maximum



# Distribution maximum

# -*- coding: utf-8 -*-

#importing libraries 
import pandas as pd 
import numpy as np
import scipy.interpolate as inter


#importe file
data=pd.read_excel('SPandBondData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=2*data['SP500'].diff(periods=-1)+3*data['Bond10'].diff(periods=-1) #compute the L&P of port
LP=data['L'].dropna() #supress the NaN of the L&P

#LP=LP.tail(1500)

#Compute the inverse of the empirical CDF, i.e. the quantile function
p = np.linspace(0,1,len(LP))                  
LossSorted = sorted(LP)
ppF = inter.interp1d(p,LossSorted)

n=len(LP)

#Compute the samples
N=10**4 #size of the samples
SampleU=np.random.uniform(0,1,size=N) #ff

SampleU=SampleU**(1/n)

#Compute the distribution of the Maximum
SampleMax=ppF(SampleU)
