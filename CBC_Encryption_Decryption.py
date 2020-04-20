#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from AES_Ciphe_InvCipher import Cipher, InvCipher
from KeyExpansion import KeyExpansion


# In[ ]:


def Bytes2Int(b):
    result = 0
    for i in b:
        result = (result << 8) | i
    return result

def Int2Bytes(n):
    result = []
    for i in range(16):
        result.append((n >> ((15-i) * 8)) & 0xff)
    return result


# In[ ]:


def CBC_Encryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=Bytes2Int(bytes(IV, 'utf-8'))
    if len(Key)!=16:
        return False
    K=Bytes2Int(bytes(Key, 'utf-8'))  
    Temp=0
    W=KeyExpansion(K)
    with open(FileName, 'rb') as rf:
        with open('Encryption.txt', 'wb') as wf:
            bytes_contents=rf.read(16)
            while len(bytes_contents)==16:
                L=Bytes2Int(bytes_contents)
                Temp=L^Initia
                Initia=Cipher(Temp, W)
                wf.write(bytes(Int2Bytes(Initia)))
                bytes_contents=rf.read(16)
            r=16-len(bytes_contents)
            L=Bytes2Int(list(bytes_contents)+r*[32])
            Temp=L^Initia
            Initia=Cipher(Temp, W)
            wf.write(bytes(Int2Bytes(Initia)))


# In[ ]:


def CBC_AES_Decryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=Bytes2Int(bytes(IV, 'utf-8'))
    if len(Key)!=16:
        return False
    K=Bytes2Int(bytes(Key, 'utf-8'))   
    Temp=0
    W=KeyExpansion(K)
    with open(FileName, 'rb') as rf:
        with open('Decryption.txt', 'wb') as wf:
            bytes_contents=rf.read(16)
            while len(bytes_contents)==16:
                L=Bytes2Int(bytes_contents)          
                Temp=InvCipher(L, W)
                wf.write(bytes(Int2Bytes(Temp^Initia)))
                Initia=L    
                bytes_contents=rf.read(16)
               


# In[ ]:




