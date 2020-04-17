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
    
    


# In[31]:


def MixCol(V):      # input 4 byte integers in a column under the basis {1, Y, Y^2...}
    PerMat=[[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]       # correspond to the basis {1, Y, Y^2..}
    r=MulMatByte(PerMat, V)       # a matrix, and should be converted into a vecor (not list...) !!!
    return r


# In[35]:


def ShiftRows(S):  # input the state matrix of Nb*colums of 4 bytes integers 
    L=[[0 for i in range(4)] for j in range(4)]  #initialization 
    for i in range(4):
        L[i][0]=S[i][0]
        L[i][1]=S[(i+1)%4][1]     # starts at the 2nd row
        L[i][2]=S[(i+2)%4][2]
        L[i][3]=S[(i+3)%4][3]
    return L         


# In[44]:


def AddMatBytes(V, W):    #Xor of two matrix of bytes integers, output still matrix of bytes integers
    U0=[[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        U0[i]=[k for k in Xor(V[i], W[i])]
    return (U0)
    


# In[64]:


def Cipher(m, w):   # input plaintext of list of 16 byte integers and expansion-key array of 11 *4=44 words of 4 byte integers as a column
    state=[[m[i] for i in range(4)], [m[i+4] for i in range(4)], [m[i+8] for i in range(4)], [m[i+12] for i in range(4)]]   #state matrix with column a_0a_1..
    state=AddMatBytes(state, [w[i] for i in range(4)])   # round 0, with first 4 columns of w
    for n in range(9):        # from round 1 to round 9
        for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[0][state[i][j]]
        state=ShiftRows(state)
        for m in range(4):
            state[m]=MixCol(state[m])
        state=AddMatBytes(state, [w[i+4*(n+1)] for i in range(4)])
    for i in range(4):             # in round 10, the SubByte using S-Box
            for j in range(4):
                state[i][j]=S_Box()[0][state[i][j]]
    state=ShiftRows(state)
    state=AddMatBytes(state, [w[i+40] for i in range(4)])
    temp=[]
    for x in range(4):
        for y in range(4):
            temp+=[state[x][y]]
    return (temp)  


# In[ ]:




