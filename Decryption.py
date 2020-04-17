#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import CBC_Decryption
import timeit

# In[ ]:


print('Please make sure the ciphertext file is in the same folder, please enter the file name: ')
FileName=input()
print('Please enter the file initial word consisting of 16 characters ( as you must know ): ')
IV=input()
print('Please enter the encryption key consisting of 16 characters ( as you must know ): ')
Key=input()
print('Please wait for a moment...')


# In[ ]:

start_time = timeit.default_timer()
CBC_Decryption.CBC_Decryption(FileName, IV, Key)


# In[ ]:


print('The decryption file named "Decryption.txt" can be found in the same folder now.')
print('The running time is: ', timeit.default_timer()-start_time)
