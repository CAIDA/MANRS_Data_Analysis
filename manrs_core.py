#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from collections import defaultdict
import bz2, gzip


# ## Download MANRS ISP list

# In[2]:


manrs = []
manrs_org = {}
manrs_org2as = defaultdict(list)
manrsisp_count = 0
with open('/project/manic-geo/irr/manrs/manrsisps.csv', 'rt') as f:  #replace with new file
    for line in f:
        data = line.strip().split(',')
        if len(data) < 7:
            continue
        manrsisp_count += 1
        asns = data[2].split(';')
        
        for i in asns:
            try:
                manrs.append(int(i))
                manrs_org[int(i)] = data[0]
                manrs_org2as[data[0]].append(int(i))
            except:
                pass


# In[3]:


manrscdn = []
manrscdn_count = 0
with open('/project/manic-geo/irr/manrs/manrscdns.csv', 'rt') as f:   #replace with new file
    for line in f:
        data = line.strip().split(',')
        if len(data) < 7:
            continue
        manrscdn_count += 1
        asns = data[1].split(';')
        for i in asns:
            if not i.isdigit():
                continue
            try:
                manrscdn.append(int(i))
                manrs_org[int(i)] = data[0]
                manrs_org2as[data[0]].append(int(i))
            except:
                pass


# In[4]:


print("Numbers of orgs in the MANRS ISP Program: ", manrsisp_count)


# In[5]:


print("Numbers of orgs in the MANRS CDN Program: ", manrscdn_count)


# In[6]:


manrsas = manrs + manrscdn


# In[7]:


manrs = manrsas


# In[8]:


print('number of MANRS ASes', len(manrsas))


# In[9]:


print('number of MANRS ASes', len(manrs))


# ## Parse AS-Relationship
# 
# Download from CAIDA https://www.caida.org/catalog/datasets/as-relationships/

# In[10]:


path = '/project/manic-geo/irr/manrs/20221201.as-rel.txt.bz2'
as_rel = defaultdict(lambda: defaultdict(set))
topAS = set()
with bz2.open(path, 'rt') as file:
    for line in file:
        if line.startswith('# input clique'):
            data = line.split(' ')
            for i in data[3:]:
                topAS.add(int(i))
        if line.startswith('#'):
            continue
        data = line.strip().split('|')
        AS1 = data[0]
        AS2 = data[1]
        rel = data[2]
        if rel == '0':
            as_rel[AS1]['peer'].add(AS2)
            as_rel[AS2]['peer'].add(AS1)
        elif rel == '1':
            as_rel[AS1]['provider'].add(AS2)
            as_rel[AS2]['customer'].add(AS1)
        elif rel == '-1':
            as_rel[AS1]['customer'].add(AS2)
            as_rel[AS2]['provider'].add(AS1)


# In[11]:


##peering clique at the top of AS hierarchy


# ## find the manrs core

# ### find the peering clique at the top of AS hierarchy that are MANRS ASes

# In[12]:


manrs_root = set()
for i in topAS:
    if i in manrs:
        manrs_root.add(i)


# In[13]:





# ### find the customers of the manrs root
# 
# recursively look for customers

# #### strict mode: for multi-homed customers, all providers must be in MANRS

# In[14]:


def check_multihome(asn):
    for i in as_rel[asn]['provider']:
        if int(i) not in manrs:
            return False
    return True


# In[15]:


def recur_manrs_customers_multihome(tc,asn):
    for i in as_rel[str(asn)]['customer']:
        if i in tc or int(i) not in manrs:
            continue
        elif check_multihome(str(i)):
            tc.add(i)
            recur_manrs_customers_multihome(tc,i)


# In[16]:


manrs_core_strict = set()
for i in manrs_root:
    recur_manrs_customers_multihome(manrs_core_strict, i)
    manrs_core_strict.add(i)


# In[17]:


print('# of MANRS core ASes where all providers of any AS are in MANRS: ', len(manrs_core_strict))


# In[18]:


manrs_core_strict_org = set()
for i in manrs_core_strict:
    manrs_core_strict_org.add(manrs_org[int(i)])


# In[19]:


print('# of MANRS core_strict organizations: ', len(manrs_core_strict_org))


# #### relaxed mode: all customers 

# In[20]:


def recur_manrs_customers(tc,asn):
    for i in as_rel[str(asn)]['customer']:
        if i in tc or int(i) not in manrs:
            continue
        else:
            tc.add(i)
            recur_manrs_customers(tc,i)


# In[21]:


manrs_core = set()
for i in manrs_root:
    recur_manrs_customers(manrs_core, i)
    manrs_core.add(i)


# In[22]:


print('# of MANRS core ASes: ', len(manrs_core))


# In[23]:


manrs_core_org = set()
for i in manrs_core:
    manrs_core_org.add(manrs_org[int(i)])


# In[24]:


print('# of MANRS core organizations: ', len(manrs_core_org))


# ## all other ASes that connect to the MANRS core (strict)

# In[25]:


def recur_customers(tc,asn):
    for i in as_rel[str(asn)]['customer']:
        if i in tc:
            continue
        else:
            tc.add(i)


# In[39]:


connected_manrs_core = set()
for i in manrs_core:
    recur_customers(connected_manrs_core, i)


# ### Download as2org dataset from CAIDA
# 
# https://www.caida.org/catalog/datasets/as-organizations/

# In[33]:


path = '/project/manic-geo/irr/manrs/20221001.as-org2info.txt.gz'
mapping = {}
companyname = {}

with gzip.open(path, 'rt') as as2org:
    for line in as2org:
        l = line.strip('\n').split('|')
        asn = None
        if l[0].isdigit():
            asn = l[0]
            mapping[asn] = l[3]
        elif len(l) == 5:
            companyname[l[0]] = (l[2], l[3])
    for i in mapping:
        orgname = companyname[mapping[i]]
        mapping[i] = orgname


# ### Count US based ASes; Map ASes to Organizations

# In[40]:


connected_manrs_core_org = set()
US_based = set()
no_org_data = set()
for i in connected_manrs_core:
    if i not in mapping:
        no_org_data.add(i)
        continue
    connected_manrs_core_org.add(mapping[i][0])
    if mapping[i][1] == 'US':
        US_based.add(i)


# In[41]:


print('# of ASes connected to the MANRS core: ', len(connected_manrs_core))


# In[42]:


print('# of organizations connected to the MANRS core: ', len(connected_manrs_core_org))


# In[37]:


print('# of US based ASes connected to the MANRS core: ', len(US_based))


# In[38]:




# In[ ]:




