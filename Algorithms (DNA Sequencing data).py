#!/usr/bin/env python
# coding: utf-8

# In[1]:


def longestCommonPrefix(s1, s2):
    i = 0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1
    return s1[:i]


# In[2]:


def match(s1 ,s2):
    if not len(s1) == len(s2):
        return False
    for i in range(len(s1)):
        if not s1[i] == s2[i]:
            return False
    return True


# In[3]:


complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}


# In[4]:


def reverseComplement(s):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    t = ''
    for base in s:
        t = complement[base] + t 
    return t


# In[5]:


def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()
    return genome
genome = readGenome("lambda_virus.fa")


# In[6]:


len(genome)


# In[8]:


import collections
collections.Counter(genome)


# In[10]:


def readFastq(filename):
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline()
            seq = fh.readline().rstrip()
            fh.readline()
            qual = fh.readline().rstrip()
            if len(seq) == 0: 
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities 


# In[11]:


seqs, quals = readFastq('SRR835775_1.first1000.fastq')


# In[12]:


print(seqs[:5])


# In[13]:


print(quals[:5])


# In[16]:


# exact matching: naive algorithm

def naive(p, t):
    occurences = []
    for i in range(len(t) - len(p) + 1):
        match = True
        for j in range(len(p)):
            if t[i+j] != p[j]:
                match = False
                break
        if match:
            occurences.append(i)
    return occurences


# In[18]:


def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()
    return genome
genome = readGenome("phix.fa") 


# In[19]:


def naive(p, t):
    occurences = []
    for i in range(len(t) - len(p) + 1):
        match = True
        for j in range(len(p)):
            if t[i+j] != p[j]:
                match = False
                break
        if match:
            occurences.append(i)
    return occurences


# In[20]:


import random
def generateReads(genome, numReads, readLen): 
    #numbReads: the number of Reads, readLen: the length of read
    ''' Generate reads from random positions in the given genome. '''
    
    reads = []
    for _ in range(numReads):
        start = random.randint(0, len(genome)-readLen) - 1
        reads.append(genome[start:start+readLen])
    return reads

