#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from S_Box import S_Box, DivByte, MulByte


# In[ ]:


def Xor(U,V):        # xor for two vectors
    L=[i for i in range(len(U))]
    for i in range(len(V)):
        L[i]=U[i]^V[i]
    return L


# In[40]:


def Ron(i):         # constructor of a vector over F_2^8
    s=1
    for n in range(i-1):
        s=MulByte(2, s)
    r=DivByte(s, 283)[0]
    return [r, 0, 0, 0]


# In[42]:


def KeyExpansion(V):   #input like the state arrow, a one dimensional list consists of 16 byte integers
    i=0
    temp=[0 for i in range(4)]
    t=[0 for i in range(4)]
    w=[[] for i in range(44)]
    while i<4:
        w[i]=[V[4*i], V[4*i+1], V[4*i+2], V[4*i+3]]  # exactly the column by the display
        i=i+1
    i=4
    while i<44:
        temp=w[i-1]
        if i%4==0:
            t=[S_Box()[0][temp[1]], S_Box()[0][temp[2]], S_Box()[0][temp[3]], S_Box()[0][temp[0]]]
            temp=Xor(t, Ron(i//4))
        w[i]=Xor(w[i-4], temp)
        i=i+1
    return w


# In[ ]:




