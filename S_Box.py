#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Int2Vect(n):        # input an integer, output the binary digits, completed in 8 digits AND V[i] with 2^i
    C=bin(n)[2:][: : -1]
    V=[0 for i in range(len(C))]
    for i in range(len(C)):
        if C[i]=='0':
            V[i]=0
        else:
            V[i]=1
    return V+(8-len(V))*[0]
        


# In[2]:


def Left_s(b, s):     # input an integer, output integer as shift leftwords by s seen as a binary ...a_1 a_0
    return b*2**s    # exactly the same meaning


# In[3]:


def Vect2Int(V):      # binary digits into integer
    s=0
    for i in range(len(V)):
        s+=V[i]*2**i
    return s


# In[4]:


def DivByte(a,b):   # division of the two bytes (already converted into integers) as elements of F_2^8 i.e polynomials
    if b==1:
        return 0, a
    if len(bin(a))<len(bin(b)):
        return a, 0
    r=a
    l=len(bin(a))-2
    q=[0 for i in range(l)]
    s=len(bin(a))-len(bin(b))
    q0=0
    while not s<0:
        q[s]=1
        r=Left_s(b, s)^r
        s=len(bin(r))-len(bin(b))
    q0=Vect2Int(q)
    return r, q0
    


# In[5]:


def X_MulByte(b):   #input one byte as integer, output Xb as integer of byte
    V=Int2Vect(b)
    l=V[7]      # coefficient of x_7 of b
    if l==0:
        return Left_s(b, 1)
    else:
        a=Left_s(b-2**7, 1)
        return (a^27)      # x^8=(0b00011011)
    
    


# In[6]:


def MulByte(a,b):    #input two bytes (as integers), ouput product as in F_2^8
    V=Int2Vect(a)
    s=0
    t=b
    for i in range(len(V)):
        if V[i]==1:
            s=t^s
        t=X_MulByte(t)
    return s
    
    


# In[7]:


def InvByte(b):     # input converted byte as integer, output the inverse byte in F_2^8
    a=283
    r0=a; r1=b
    U0=1; U1=0
    V0=0; V1=1
    r,q,U,V=0,0,0,0
    while not r1==0:        
        q=DivByte(r0, r1)[1]
        r=DivByte(r0, r1)[0]
        r0=r1; r1=r
        U=U0^MulByte(q, U1)
        V=V0^MulByte(q, V1)
        U0=U1; V0=V1
        U1=U; V1=V   # r1=U1*a+V1*b
    return V0 # r0=U0*a+V0*b


# In[8]:


def MulMat(M, V):         # matrix over F_2
    r=len(M)
    c=len(M[0])
    s=[0 for k in range(r)]
    for i in range(r):
        for j in range(c):
            s[i]=(M[i][j]*V[j])^s[i]
    return s
    


# In[9]:


def AddVect(V,W):
    S=[0 for i in range(len(V))]
    for j in range(len(V)):
        S[j]=V[j]^W[j]
    return S


# In[10]:


def SubByte(byte_int):   # input byte integer, output byte INTEGER
    V=Int2Vect(byte_int)      
    M=[[1,0,0,0,1,1,1,1], [1,1,0,0,0,1,1,1], [1,1,1,0,0,0,1,1], [1,1,1,1,0,0,0,1], [1,1,1,1,1,0,0,0], [0,1,1,1,1,1,0,0], [0,0,1,1,1,1,1,0], [0,0,0,1,1,1,1,1]]
    C=[1,1,0,0,0,1,1,0]
    if byte_int==0:
        return Vect2Int(C)
    else:
        V0=Int2Vect(InvByte(byte_int))    # By def, v^-1 here. And the vector follows the basis order in sage
        R=AddVect(MulMat(M, V0), C)
        return Vect2Int(R)


# In[11]:


def InvSubByte(byte_int):     # input byte integer, output byte INTEGER
    V=Int2Vect(byte_int)      
    iM=[[0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0]]
    C=[1,1,0,0,0,1,1,0]
    if byte_int==99:
        return 0
    else:
        R=MulMat(iM, AddVect(V, C))
        n=InvByte(Vect2Int(R))
        return n


# In[12]:


def S_Box():
    S=[' ' for i in range(256)]
    iS=[' ' for j in range(256)]
    for i in range(256):
        el1=SubByte(i)
        el2=InvSubByte(i)
        S[i]=el1
        iS[i]=el2
    return S, iS 


# In[13]:


S_Box()

