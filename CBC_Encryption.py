#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from AES_Cipher import Cipher
from KeyExpansion import KeyExpansion, Xor


# In[58]:


def CBC_Encryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=list(bytes(IV, 'utf-8'))
    if len(Key)!=16:
        return False
    K=list(bytes(Key, 'utf-8'))  
    Temp=[0 for i in range(16)]
    W=KeyExpansion(K)
    with open(FileName, 'rb') as rf:
        with open('Encryption.txt', 'wb') as wf:
            bytes_contents=rf.read(16)
            while len(bytes_contents)==16:
                L=list(bytes_contents)
                Temp=Xor(L, Initia)
                Initia=Cipher(Temp, W)
                wf.write(bytes(Initia))
                bytes_contents=rf.read(16)
            r=16-len(bytes_contents)
            L=list(bytes_contents)+r*[32]
            Temp=Xor(L, Initia)
            Initia=Cipher(Temp, W)
            wf.write(bytes(Initia))


# In[ ]:




