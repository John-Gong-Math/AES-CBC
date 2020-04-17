#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from AES_InvCipher import InvCipher
from KeyExpansion import KeyExpansion, Xor


# In[62]:


def CBC_Decryption(FileName, IV, Key):   # input the filename with .txt format, IV, Key as strings
    if len(IV)!=16:
        return False
    Initia=list(bytes(IV, 'utf-8'))
    if len(Key)!=16:
        return False
    K=list(bytes(Key, 'utf-8'))   
    Temp=[0 for i in range(16)]
    W=KeyExpansion(K)
    with open(FileName, 'rb') as rf:
        with open('Decryption.txt', 'wb') as wf:
            bytes_contents=rf.read(16)
            while len(bytes_contents)==16:
                L=list(bytes_contents)          
                Temp=InvCipher(L, W)
                wf.write(bytes(Xor(Temp, Initia)))
                Initia=L    
                bytes_contents=rf.read(16)
               


# In[ ]:




