#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from S_Box import S_Box, MulByte
from KeyExpansion import Xor


# In[29]:


def MulMatByte(M, V):  # for matrix of byte integers i.e over F_2^8
    r=len(M)
    c=len(M[0])
    s=[0 for k in range(r)]
    for i in range(r):
        for j in range(c):
            s[i]=(MulByte(M[i][j], V[j]))^s[i]
    return s
    
    


# In[33]:


def InvMixCol(V):
    InvPerMat=[[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]
    r=MulMatByte(InvPerMat, V)
    return r


# In[37]:


def InvShiftRows(S):
    L=[[0 for i in range(4)] for j in range(4)]  #initialization 
    for i in range(4):
        L[i][0]=S[i][0]
        L[i][1]=S[(i-1)%4][1]     # starts at the 2nd row
        L[i][2]=S[(i-2)%4][2]
        L[i][3]=S[(i-3)%4][3]
    return L            


# In[44]:


def AddMatBytes(V, W):    #Xor of two matrix of bytes integers, output still matrix of bytes integers
    U0=[[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        U0[i]=[k for k in Xor(V[i], W[i])]
    return (U0)
    


# In[66]:


def InvCipher(m,w):
    state=[[m[i] for i in range(4)], [m[i+4] for i in range(4)], [m[i+8] for i in range(4)], [m[i+12] for i in range(4)]]   #state matrix with column a_0a_1..
    state=AddMatBytes(state, [w[i+40] for i in range(4)])
    for n in range(9):
        state=InvShiftRows(state)
        for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[1][state[i][j]]
        state=AddMatBytes(state, [w[i+4*(9-n)] for i in range(4)])
        for i in range(4):
            state[i]=InvMixCol(state[i])
    state=InvShiftRows(state)
    for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[1][state[i][j]]
    state=AddMatBytes(state, [w[i] for i in range(4)])  
    temp=[]
    for x in range(4):
        for y in range(4):
            temp+=[state[x][y]]
    return (temp)   


# In[ ]:




