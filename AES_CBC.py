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
        


# In[3]:


def Left_s(b, s):     # input an integer, output integer as shift leftwords by s seen as a binary ...a_1 a_0
    return b*2**s    # exactly the same meaning


# In[5]:


def Vect2Int(V):      # binary digits into integer
    s=0
    for i in range(len(V)):
        s+=V[i]*2**i
    return s


# In[6]:


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
    


# In[9]:


def X_MulByte(b):   #input one byte as integer, output Xb as integer of byte
    V=Int2Vect(b)
    l=V[7]      # coefficient of x_7 of b
    if l==0:
        return Left_s(b, 1)
    else:
        a=Left_s(b-2**7, 1)
        return (a^27)      # x^8=(0b00011011)
    
    


# In[10]:


def MulByte(a,b):    #input two bytes (as integers), ouput product as in F_2^8
    V=Int2Vect(a)
    s=0
    t=b
    for i in range(len(V)):
        if V[i]==1:
            s=t^s
        t=X_MulByte(t)
    return s
    
    


# In[12]:


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


# In[19]:


def MulMat(M, V):         # matrix over F_2
    r=len(M)
    c=len(M[0])
    s=[0 for k in range(r)]
    for i in range(r):
        for j in range(c):
            s[i]=(M[i][j]*V[j])^s[i]
    return s
    


# In[20]:


def AddVect(V,W):
    S=[0 for i in range(len(V))]
    for j in range(len(V)):
        S[j]=V[j]^W[j]
    return S


# In[21]:


def SubByte(hexa):   # input string byte hex, output hex string byte
    V=Int2Vect(int(hexa,16))      
    M=[[1,0,0,0,1,1,1,1], [1,1,0,0,0,1,1,1], [1,1,1,0,0,0,1,1], [1,1,1,1,0,0,0,1], [1,1,1,1,1,0,0,0], [0,1,1,1,1,1,0,0], [0,0,1,1,1,1,1,0], [0,0,0,1,1,1,1,1]]
    C=[1,1,0,0,0,1,1,0]
    if hexa=='0x0':
        return hex(Vect2Int(C))
    else:
        V0=Int2Vect(InvByte(int(hexa, 16)))    # By def, v^-1 here. And the vector follows the basis order in sage
        R=AddVect(MulMat(M, V0), C)
        return hex(Vect2Int(R))     


# In[23]:


def InvSubByte(hexa):
    V=Int2Vect(int(hexa,16))      
    iM=[[0, 0, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 1, 0]]
    C=[1,1,0,0,0,1,1,0]
    if hexa=='0x63':
        return '0x0'
    else:
        R=MulMat(iM, AddVect(V, C))
        n=InvByte(Vect2Int(R))
        return hex(n)     


# In[25]:


def S_Box():
    S=[' ' for i in range(256)]
    iS=[' ' for j in range(256)]
    for i in range(256):
        el0=hex(i)
        el1=SubByte(el0)
        el2=InvSubByte(el0)
        S[i]=el1
        iS[i]=el2
    return S, iS 


# In[26]:


S_Box()


# In[29]:


def MulMatByte(M, V):  # for matrix of integer bytes i.e over F_2^8
    r=len(M)
    c=len(M[0])
    s=[0 for k in range(r)]
    for i in range(r):
        for j in range(c):
            s[i]=(MulByte(M[i][j], V[j]))^s[i]
    return s
    
    


# In[30]:


PerMat=[[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]   # correspond to the basis {1, Y, Y^2..}


# In[31]:


def MixCol(V):      # input 4 bytes in a column, each noted by string format, under the basis {1, Y, Y^2...}
    W=[int(i, 16) for i in V]       # bytes intepreted as integers
    PerMat=[[2,3,1,1], [1,2,3,1], [1,1,2,3], [3,1,1,2]]       # correspond to the basis {1, Y, Y^2..}
    r=MulMatByte(PerMat, W)       # a matrix, and should be converted into a vecor (not list...) !!!
    return [hex(i) for i in r]


# In[33]:


def InvMixCol(V):
    W=[int(i, 16) for i in V] 
    InvPerMat=[[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]
    r=MulMatByte(InvPerMat, W)
    return [hex(i) for i in r]


# In[35]:


def ShiftRows(S):  # input the state matrix of Nb*colums of 4 bytes a_0, a_1 ..., always in string format
    L=[['' for i in range(4)] for j in range(4)]  #initialization 
    for i in range(4):
        L[i][0]=S[i][0]
        L[i][1]=S[(i+1)%4][1]     # starts at the 2nd row
        L[i][2]=S[(i+2)%4][2]
        L[i][3]=S[(i+3)%4][3]
    return L         


# In[37]:


def InvShiftRows(S):
    L=[['' for i in range(4)] for j in range(4)]  #initialization 
    for i in range(4):
        L[i][0]=S[i][0]
        L[i][1]=S[(i-1)%4][1]     # starts at the 2nd row
        L[i][2]=S[(i-2)%4][2]
        L[i][3]=S[(i-3)%4][3]
    return L            


# In[39]:


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


def KeyExpansion(V):   #input like the state arrow, a one dimensional list consists of bytes
    i=0
    temp=[0 for i in range(4)]
    t=[0 for i in range(4)]
    K=[int(i, 16) for i in V]
    Sb=[int(i, 16) for i in S_Box()[0]]
    w=[[] for i in range(44)]
    wc=[['' for i in range(4)] for k in range(44)]
    while i<4:
        w[i]=[K[4*i], K[4*i+1], K[4*i+2], K[4*i+3]]  # exactly the column by the display
        i=i+1
    i=4
    while i<44:
        temp=w[i-1]
        if i%4==0:
            t=[Sb[temp[1]], Sb[temp[2]], Sb[temp[3]], Sb[temp[0]]]
            temp=Xor(t, Ron(i//4))
        w[i]=Xor(w[i-4], temp)
        i=i+1
    for n in range(44):
        for m in range(4):
            wc[n][m]=hex(w[n][m])
    return wc


# In[44]:


def AddMatBytes(V, W):    #Xor of two matrix of hex bytes, output still matrix of hex bytes
    V0=[[0,0,0,0] for i in range(4)]
    W0=[[0,0,0,0] for i in range(4)]
    U0=[['' for i in range(4)] for j in range(4)]
    for i in range(4):
        V0[i]=[int(i, 16) for i in V[i]]
        W0[i]=[int(i, 16) for i in W[i]]
        U0[i]=[hex(k) for k in Xor(V0[i], W0[i])]
    return (U0)
    


# In[46]:


def Cipher(m, w):   # input plaintext of list of 16 bytes and expansion-key array of 11 *4=44 words of 4 bytes as a column
    state=[[m[i] for i in range(4)], [m[i+4] for i in range(4)], [m[i+8] for i in range(4)], [m[i+12] for i in range(4)]]   #state matrix with column a_0a_1..
    state=AddMatBytes(state, [w[i] for i in range(4)])   # round 0, with first 4 columns of w
    for n in range(9):        # from round 1 to round 9
        for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[0][int(state[i][j], 16)]
        state=ShiftRows(state)
        for m in range(4):
            state[m]=MixCol(state[m])
        state=AddMatBytes(state, [w[i+4*(n+1)] for i in range(4)])
    for i in range(4):             # in round 10, the SubByte using S-Box
            for j in range(4):
                state[i][j]=S_Box()[0][int(state[i][j], 16)]
    state=ShiftRows(state)
    state=AddMatBytes(state, [w[i+40] for i in range(4)])
    temp=[]
    for x in range(4):
        for y in range(4):
            temp+=[state[x][y]]
    return (temp)  


# In[48]:


def InvCipher(m,w):
    state=[[m[i] for i in range(4)], [m[i+4] for i in range(4)], [m[i+8] for i in range(4)], [m[i+12] for i in range(4)]]   #state matrix with column a_0a_1..
    state=AddMatBytes(state, [w[i+40] for i in range(4)])
    for n in range(9):
        state=InvShiftRows(state)
        for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[1][int(state[i][j], 16)]
        state=AddMatBytes(state, [w[i+4*(9-n)] for i in range(4)])
        for i in range(4):
            state[i]=InvMixCol(state[i])
    state=InvShiftRows(state)
    for i in range(4):    
            for j in range(4):
                state[i][j]=S_Box()[1][int(state[i][j], 16)]
    state=AddMatBytes(state, [w[i] for i in range(4)])  
    temp=[]
    for x in range(4):
        for y in range(4):
            temp+=[state[x][y]]
    return (temp)   


# In[55]:


def CBC_AES_Encryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=[hex(i) for i in list(bytes(IV, 'utf-8'))]
    if len(Key)!=16:
        return False
    K=[hex(i) for i in list(bytes(Key, 'utf-8'))]    #convert to hexadecimal bytes
    Temp=['' for i in range(16)]
    W=KeyExpansion(K)
    with open(FileName, 'rb') as rf:
        with open('Encryption.txt', 'wb') as wf:
            bytes_contents=rf.read()
            r=len(bytes_contents)%16
            L=list(bytes_contents)+(16-r)*[32]
            n=len(L)//16
            for m in range(n):
                Temp=[hex(i) for i in Xor([L[s+m*16] for s in range(16)], [int(j, 16) for j in Initia])]
                Initia=Cipher(Temp, W)
                wf.write(bytes([int(i, 16) for i in Initia]))


# In[62]:


def CBC_AES_Decryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=list(bytes(IV, 'utf-8'))
    if len(Key)!=16:
        return False
    K=[hex(i) for i in list(bytes(Key, 'utf-8'))]    #convert to hexadecimal bytes
    Temp=['' for i in range(16)]
    W=KeyExpansion(K)
    with open('Encryption.txt', 'rb') as rf:
        with open('Decryption.txt', 'wb') as wf:
            bytes_contents=rf.read()
            L=list(bytes_contents)          
            if len(L)%16 !=0:
                return False
            n=len(L)//16
            for m in range(n):
                Temp=InvCipher([hex(i) for i in [L[j+m*16] for j in range(16)]], W)
                wf.write(bytes(Xor([int(i, 16) for i in Temp], Initia)))
                Initia=[L[i+m*16] for i in range(16)]     # list of integers


# In[ ]:




