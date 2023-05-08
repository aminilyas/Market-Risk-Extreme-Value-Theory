# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 18:25:36 2022

@author: Esteban Lopez
"""


#3.1d

# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

#importe file
data=pd.read_excel('SPandBondData.xlsx',sheet_name='Price') #read the data into a panda DataFrame


#Compute L&P
data['L']=2*data['SP500'].diff(periods=-1)+3*data['Bond10'].diff(periods=-1) #compute the L&P of port

#Arange data in descending order
data = data.sort_values(by=['L'], ascending=False)
data= data.reset_index(drop=True)


k=10
Hill10=np.log(data['L'][0])
for i in range(1,k):
    Hill10=Hill10+np.log(data['L'][i])

Hill10=1/k*Hill10-np.log(data['L'][k+1])

k=11
Hill11=np.log(data['L'][0])
for i in range(1,k):
    Hill11=Hill11+np.log(data['L'][i])

Hill11=1/k*Hill11-np.log(data['L'][k+1])

k=12
Hill12=np.log(data['L'][0])
for i in range(1,k):
    Hill12=Hill12+np.log(data['L'][i])

Hill12=1/k*Hill12-np.log(data['L'][k+1])

k=13
Hill13=np.log(data['L'][0])
for i in range(1,k):
    Hill13=Hill13+np.log(data['L'][i])

Hill13=1/k*Hill13-np.log(data['L'][k+1])

k=14
Hill14=np.log(data['L'][0])
for i in range(1,k):
    Hill14=Hill14+np.log(data['L'][i])

Hill14=1/k*Hill14-np.log(data['L'][k+1])

k=15
Hill15=np.log(data['L'][0])
for i in range(1,k):
    Hill15=Hill15+np.log(data['L'][i])

Hill15=1/k*Hill15-np.log(data['L'][k+1])

HillVec=np.array([Hill10, Hill11, Hill12,Hill13, Hill14, Hill15])

Hill=HillVec.mean()

print('The Hill estimate of Xsi is',Hill)


k=2
Hill2=np.log(data['L'][0])
for i in range(1,k):
    Hill2=Hill2+np.log(data['L'][i])

Hill2=1/k*Hill2-np.log(data['L'][k+1])





