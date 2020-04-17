#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import CBC_Encryption
import timeit


# In[ ]:


print('Please make sure the plaintext file is in the same folder, please enter the file name: ')
FileName=input()
print('Please enter the file initial word consisting of 16 characters ( keep it well ): ')
IV=input()
print('Please enter the encryption key consisting of 16 characters ( keep it well ): ')
Key=input()
print('Please wait for a moment...')


# In[ ]:


start_time = timeit.default_timer()


# In[ ]:


CBC_Encryption.CBC_Encryption(FileName, IV, Key)


# In[ ]:


print('The encryption file named "Encryption.txt" can be found in the same folder now.')


# In[ ]:


print('The running time is: ', timeit.default_timer()-start_time)

